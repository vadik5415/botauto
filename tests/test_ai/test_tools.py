from ai.tools.cost_calculator import CostCalculator


def test_shipping_multiplier_for_expensive_car():
    calc = CostCalculator(customs_data={}, shipping_data={})
    result = calc.calculate_total_cost(car_price_usd=60000, engine_volume=2.5, year=2020)
    assert result["shipping"] == 1560
