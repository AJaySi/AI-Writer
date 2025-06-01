from typing import Dict, Any, List, Optional
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiohttp
import json
from .error_handling import PlatformError

logger = logging.getLogger('content_scheduler')

class NotificationManager:
    """Manages notifications for scheduled content."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize notification manager with configuration."""
        self.config = config
        self.email_config = config.get('email', {})
        self.slack_config = config.get('slack', {})
        self.webhook_config = config.get('webhook', {})
    
    async def send_notification(
        self,
        event_type: str,
        content: Dict[str, Any],
        channels: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send notification through specified channels."""
        results = {}
        
        for channel in channels:
            try:
                if channel == 'EMAIL':
                    results['email'] = await self._send_email_notification(
                        event_type, content, metadata
                    )
                elif channel == 'SLACK':
                    results['slack'] = await self._send_slack_notification(
                        event_type, content, metadata
                    )
                elif channel == 'WEBHOOK':
                    results['webhook'] = await self._send_webhook_notification(
                        event_type, content, metadata
                    )
                else:
                    logger.warning(f"Unsupported notification channel: {channel}")
            except Exception as e:
                logger.error(f"Failed to send {channel} notification: {str(e)}")
                results[channel] = {
                    'success': False,
                    'error': str(e)
                }
        
        return results
    
    async def _send_email_notification(
        self,
        event_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send email notification."""
        if not self.email_config:
            raise PlatformError(
                "Email configuration not found",
                {'event_type': event_type}
            )
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = self.email_config['to_email']
            msg['Subject'] = self._get_email_subject(event_type, content)
            
            body = self._format_email_body(event_type, content, metadata)
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(
                self.email_config['smtp_server'],
                self.email_config['smtp_port']
            ) as server:
                if self.email_config.get('use_tls'):
                    server.starttls()
                if self.email_config.get('username'):
                    server.login(
                        self.email_config['username'],
                        self.email_config['password']
                    )
                server.send_message(msg)
            
            return {'success': True}
        except Exception as e:
            raise PlatformError(
                f"Failed to send email notification: {str(e)}",
                {
                    'event_type': event_type,
                    'error': str(e)
                }
            )
    
    async def _send_slack_notification(
        self,
        event_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send Slack notification."""
        if not self.slack_config:
            raise PlatformError(
                "Slack configuration not found",
                {'event_type': event_type}
            )
        
        try:
            message = self._format_slack_message(event_type, content, metadata)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.slack_config['webhook_url'],
                    json=message
                ) as response:
                    if response.status != 200:
                        raise PlatformError(
                            f"Slack API returned status {response.status}",
                            {'response': await response.text()}
                        )
                    return {'success': True}
        except Exception as e:
            raise PlatformError(
                f"Failed to send Slack notification: {str(e)}",
                {
                    'event_type': event_type,
                    'error': str(e)
                }
            )
    
    async def _send_webhook_notification(
        self,
        event_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send webhook notification."""
        if not self.webhook_config:
            raise PlatformError(
                "Webhook configuration not found",
                {'event_type': event_type}
            )
        
        try:
            payload = self._format_webhook_payload(event_type, content, metadata)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_config['url'],
                    json=payload,
                    headers=self.webhook_config.get('headers', {})
                ) as response:
                    if response.status != 200:
                        raise PlatformError(
                            f"Webhook returned status {response.status}",
                            {'response': await response.text()}
                        )
                    return {'success': True}
        except Exception as e:
            raise PlatformError(
                f"Failed to send webhook notification: {str(e)}",
                {
                    'event_type': event_type,
                    'error': str(e)
                }
            )
    
    def _get_email_subject(
        self,
        event_type: str,
        content: Dict[str, Any]
    ) -> str:
        """Generate email subject based on event type."""
        subjects = {
            'ON_SUCCESS': f"Content Published Successfully: {content.get('title', 'Untitled')}",
            'ON_FAILURE': f"Content Publication Failed: {content.get('title', 'Untitled')}",
            'ON_RETRY': f"Content Publication Retry: {content.get('title', 'Untitled')}",
            'ON_CANCELLATION': f"Content Publication Cancelled: {content.get('title', 'Untitled')}"
        }
        return subjects.get(event_type, f"Content Update: {content.get('title', 'Untitled')}")
    
    def _format_email_body(
        self,
        event_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Format email body."""
        template = f"""
        <html>
            <body>
                <h2>Content Update Notification</h2>
                <p><strong>Event Type:</strong> {event_type}</p>
                <p><strong>Content Title:</strong> {content.get('title', 'Untitled')}</p>
                <p><strong>Platform:</strong> {content.get('platform', 'Unknown')}</p>
                <p><strong>Status:</strong> {content.get('status', 'Unknown')}</p>
        """
        
        if metadata:
            template += "<h3>Additional Details:</h3><ul>"
            for key, value in metadata.items():
                template += f"<li><strong>{key}:</strong> {value}</li>"
            template += "</ul>"
        
        template += """
            </body>
        </html>
        """
        
        return template
    
    def _format_slack_message(
        self,
        event_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format Slack message."""
        message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": self._get_email_subject(event_type, content)
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Event Type:*\n{event_type}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Platform:*\n{content.get('platform', 'Unknown')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Status:*\n{content.get('status', 'Unknown')}"
                        }
                    ]
                }
            ]
        }
        
        if metadata:
            fields = []
            for key, value in metadata.items():
                fields.append({
                    "type": "mrkdwn",
                    "text": f"*{key}:*\n{value}"
                })
            message["blocks"].append({
                "type": "section",
                "fields": fields
            })
        
        return message
    
    def _format_webhook_payload(
        self,
        event_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format webhook payload."""
        payload = {
            'event_type': event_type,
            'content': content,
            'timestamp': datetime.now(pytz.UTC).isoformat()
        }
        
        if metadata:
            payload['metadata'] = metadata
        
        return payload 