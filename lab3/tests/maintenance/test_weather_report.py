from lab3.domain.maintenance.weather_report import WeatherReport


def test_weather_report():
    w_ok = WeatherReport(temperature_c=22.0, wind_speed_ms=8.0, visibility_m=6000.0, is_stormy=False)
    assert w_ok.is_safe_for_operations is True

    w_storm = WeatherReport(temperature_c=18.0, wind_speed_ms=10.0, visibility_m=5000.0, is_stormy=True)
    assert w_storm.is_safe_for_operations is False

    w_wind = WeatherReport(temperature_c=15.0, wind_speed_ms=28.0, visibility_m=5000.0, is_stormy=False)
    assert w_wind.is_safe_for_operations is False

    w_fog = WeatherReport(temperature_c=10.0, wind_speed_ms=4.0, visibility_m=350.0, is_stormy=False)
    assert w_fog.is_safe_for_operations is False
