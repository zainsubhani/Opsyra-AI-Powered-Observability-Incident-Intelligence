"""Sentry wiring shared by every Opsyra service.

Instrumentation is opt-in: with no ``SENTRY_DSN`` configured, :func:`init_sentry`
does nothing at all, so local development, tests and CI behave exactly as before.

Log records become breadcrumbs rather than events (``event_level=None``). Events
are only created by unhandled exceptions and by explicit ``capture_exception``
calls, which keeps one failure from being reported twice.
"""

import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from opsyra_common.config import get_shared_settings


def init_sentry(service_slug: str, version: str = "0.0.0") -> bool:
    """Initialise Sentry for one service.

    Returns True when Sentry was enabled, False when no DSN is configured.
    """
    settings = get_shared_settings()
    if not settings.sentry_dsn:
        return False

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.sentry_environment,
        release=f"{service_slug}@{version}",
        traces_sample_rate=settings.sentry_traces_sample_rate,
        send_default_pii=False,
        integrations=[
            LoggingIntegration(level=logging.INFO, event_level=None),
        ],
    )
    sentry_sdk.set_tag("service", service_slug)
    return True
