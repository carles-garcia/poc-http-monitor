from alert import Alert


def test_alert_raised() -> None:
    alert = Alert(1000)
    assert not alert.active
    alert.check(1500)
    assert alert.active
    assert alert.raised()
    assert not alert.recovered()


def test_alert_not_raised() -> None:
    alert = Alert(1000)
    assert not alert.active
    alert.check(900)
    assert not alert.active
    assert not alert.raised()
    assert not alert.recovered()


def test_alert_recovered() -> None:
    alert = Alert(1000)
    alert.active = True
    alert.check(800)
    assert not alert.active
    assert alert.recovered()
    assert not alert.raised()
