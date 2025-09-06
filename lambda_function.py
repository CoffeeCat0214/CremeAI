import json
import logging
import os
import base64

try:
    from nacl.signing import VerifyKey
    from nacl.exceptions import BadSignatureError
    NACL_AVAILABLE = True
except Exception:  # pragma: no cover
    NACL_AVAILABLE = False

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY", "")

def verify_signature(event, body_bytes: bytes) -> bool:
    """Verify Discord signature using Ed25519.

    - Uses `X-Signature-Ed25519` and `X-Signature-Timestamp` headers.
    - Message to verify is timestamp + raw body bytes.
    - If PyNaCl isn't available, log a warning and allow (to avoid blocking URL verification),
      but this should be enabled for production.
    """
    try:
        headers_in = event.get("headers") or {}
        headers = {str(k).lower(): v for k, v in headers_in.items()}
        signature = headers.get("x-signature-ed25519")
        timestamp = headers.get("x-signature-timestamp")

        if not signature or not timestamp:
            logger.warning("Missing Discord signature headers: sig=%s, ts_present=%s", bool(signature), bool(timestamp))
            return False

        if not DISCORD_PUBLIC_KEY:
            logger.warning("DISCORD_PUBLIC_KEY env var not set; skipping signature verification")
            return True

        if not NACL_AVAILABLE:
            logger.warning("PyNaCl not available; skipping signature verification (enable in production)")
            return True

        logger.info(
            "Verifying Discord signature: headers=%s, body_len=%d, ts_len=%d, sig_len=%d",
            list(headers.keys())[:8], len(body_bytes), len(timestamp or ""), len(signature or "")
        )

        verify_key = VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))
        verify_key.verify(timestamp.encode() + body_bytes, bytes.fromhex(signature))
        return True
    except BadSignatureError:
        logger.warning("Invalid Discord request signature (BadSignatureError)")
        return False
    except Exception as e:
        logger.error(f"Verification error: {str(e)}")
        return False

def handle_command(body):
    """Handle Discord command"""
    try:
        command = body.get('data', {}).get('name', '')
        
        if command == 'chat':
            message = body.get('data', {}).get('options', [{}])[0].get('value', '')
            response = f"Meow! You said: {message}"
        elif command == 'decree':
            response = "By royal decree, I declare this server to be under my purr-fect rule! 👑"
        else:
            response = "Meow? I don't understand that command!"
        
        return {
            'type': 4,  # CHANNEL_MESSAGE_WITH_SOURCE
            'data': {
                'content': response
            }
        }
    except Exception as e:
        logger.error(f"Command error: {str(e)}")
        return {
            'type': 4,
            'data': {
                'content': "Meow? Something went wrong!"
            }
        }

def lambda_handler(event, context):
    """AWS Lambda handler"""
    try:
        # Minimal event logging to avoid huge payloads in logs
        try:
            logger.info(
                "Event meta: keys=%s, isB64=%s, header_keys=%s",
                list((event or {}).keys()),
                (event or {}).get("isBase64Encoded"),
                list(((event or {}).get("headers") or {}).keys())[:8]
            )
        except Exception:
            pass
        
        # Prepare raw body bytes for signature verification
        raw_body = event.get("body", "")
        if event.get("isBase64Encoded") is True:
            body_bytes = base64.b64decode(raw_body)
            body_str = body_bytes.decode("utf-8")
        else:
            body_str = raw_body if isinstance(raw_body, str) else str(raw_body)
            body_bytes = body_str.encode("utf-8")

        body = json.loads(body_str or "{}")

        # Verify signature for all requests (including PING)
        if not verify_signature(event, body_bytes):
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'invalid request signature'})
            }
        
        # Handle Discord PING after verification
        if body.get('type') == 1:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'type': 1})
            }

        # Other types
        # Handle commands
        if body.get('type') == 2:  # APPLICATION_COMMAND
            response = handle_command(body)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(response)
            }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'type': 1})
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
