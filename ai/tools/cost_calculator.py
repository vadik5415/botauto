from typing import Dict


class CostCalculator:
    """Калькулятор полной стоимости привоза автомобиля."""

    def __init__(self, customs_data: Dict, shipping_data: Dict):
        self.customs_data = customs_data
        self.shipping_data = shipping_data

    def calculate_total_cost(
        self,
        car_price_usd: float,
        engine_volume: float,
        year: int,
        country_import: str = "russia",
        country_export: str = "usa",
        is_electric: bool = False,
    ) -> Dict[str, float]:
        """Рассчитывает полную стоимость автомобиля под ключ."""
        car_cost = car_price_usd
        shipping_cost = self._calculate_shipping(country_export, country_import, car_price_usd)

        if country_import.lower() == "russia":
            customs_duty = self._calculate_customs_duty_russia(car_price_usd, engine_volume, year, is_electric)
            recycling_fee = self._calculate_recycling_fee_russia(engine_volume, year, is_electric)
            excise = self._calculate_excise_russia(engine_volume)
            vat = (car_price_usd + customs_duty + excise) * 0.20
        else:
            customs_duty = car_price_usd * 0.15
            recycling_fee = 1000
            excise = 0
            vat = car_price_usd * 0.12

        certification_cost = 800 if country_import.lower() == "russia" else 500
        company_commission = 2500
        additional_costs = 500

        total = car_cost + shipping_cost + customs_duty + recycling_fee + excise + vat + certification_cost + company_commission + additional_costs

        return {
            "car_price": round(car_cost, 2),
            "shipping": round(shipping_cost, 2),
            "customs_duty": round(customs_duty, 2),
            "recycling_fee": round(recycling_fee, 2),
            "excise": round(excise, 2),
            "vat": round(vat, 2),
            "certification": round(certification_cost, 2),
            "commission": round(company_commission, 2),
            "additional": round(additional_costs, 2),
            "total": round(total, 2),
        }

    def _calculate_customs_duty_russia(self, price: float, engine: float, year: int, is_electric: bool) -> float:
        age = 2026 - year
        if is_electric:
            return price * 0.15
        if age > 3:
            if engine <= 1.0:
                rate = 1.5
            elif engine <= 1.5:
                rate = 1.7
            elif engine <= 1.8:
                rate = 2.5
            elif engine <= 2.3:
                rate = 2.7
            elif engine <= 3.0:
                rate = 3.0
            else:
                rate = 3.6
            duty = engine * 1000 * rate * 1.1
            return max(duty, price * 0.30)
        return price * 0.30

    def _calculate_recycling_fee_russia(self, engine: float, year: int, is_electric: bool) -> float:
        age = 2026 - year
        base_rate = 20000 if age <= 3 else 5200
        if is_electric:
            multiplier = 0.17
        elif engine <= 2.0:
            multiplier = 1.5
        elif engine <= 3.0:
            multiplier = 3.1
        else:
            multiplier = 5.2
        return base_rate * multiplier

    def _calculate_excise_russia(self, engine: float) -> float:
        if engine > 3.5:
            return 1500 * ((engine - 3.5) * 1000 / 0.75)
        return 0

    def _calculate_shipping(self, from_country: str, to_country: str, car_value: float) -> float:
        routes = {
            ("usa", "russia"): 1200,
            ("japan", "russia"): 800,
            ("germany", "russia"): 1500,
            ("korea", "russia"): 900,
        }
        base_cost = routes.get((from_country.lower(), to_country.lower()), 1000)
        if car_value > 50000:
            base_cost *= 1.3
        return base_cost

    def format_calculation_for_message(self, calc: Dict[str, float]) -> str:
        """Форматирует расчет в удобный вид для Telegram."""
        excise_line = f"• Акциз: ${calc['excise']:,.0f}\n" if calc["excise"] > 0 else ""
        return (
            "📊 Детальный расчет стоимости:\n\n"
            f"• Автомобиль: ${calc['car_price']:,.0f}\n"
            f"• Доставка: ${calc['shipping']:,.0f}\n"
            f"• Таможенная пошлина: ${calc['customs_duty']:,.0f}\n"
            f"• Утилизационный сбор: ${calc['recycling_fee']:,.0f}\n"
            f"{excise_line}"
            f"• НДС: ${calc['vat']:,.0f}\n"
            f"• Сертификация (СБКТС): ${calc['certification']:,.0f}\n"
            f"• Наша комиссия: ${calc['commission']:,.0f}\n"
            f"• Дополнительные расходы: ${calc['additional']:,.0f}\n"
            "─────────────────\n"
            f"💰 ИТОГО под ключ: ${calc['total']:,.0f}\n\n"
            "⚠️ Это примерный расчет. Точная стоимость зависит от автомобиля и курсов валют."
        )
