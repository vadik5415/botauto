from ai.tools.cost_calculator import CostCalculator


def test_calculate_total_cost_has_total():
    calculator = CostCalculator(customs_data={}, shipping_data={})
    data = calculator.calculate_total_cost(car_price_usd=15000, engine_volume=1.8, year=2019)
    assert data["total"] > data["car_price"]
