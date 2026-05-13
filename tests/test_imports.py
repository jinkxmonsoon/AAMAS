"""Lightweight import tests for package skeleton integrity."""


def test_package_imports() -> None:
    import cctdiag  # noqa: F401
    import cctdiag.io  # noqa: F401
    import cctdiag.schema  # noqa: F401
    import cctdiag.metrics  # noqa: F401
    import cctdiag.stats  # noqa: F401
    import cctdiag.reporting  # noqa: F401
