from src.engine.workflows.RvB.Comparator import Comparator

class RvBTool:
    def __init__(
        self,
        purchase_price: float,
        sqm: int,
        condo_owner_fees_coeff: float,
        notary_fees: float,
        payback_years: int,
        years_occurring_renovation: int,
        mortgage_interest_rate: float,
        price_to_rent_coeff: float,
        avg_price_sqm: float,
        cadastral_value_coefficient: float = 2.18,
        avg_invest_return: float = 0.05,
        buying_from_individual: str = "Privato",
        tax_deduction: float = 0.0
    ):
        
        self._comparator = Comparator(
            purchase_price,
            sqm,
            condo_owner_fees_coeff,
            notary_fees,
            payback_years,
            years_occurring_renovation,
            mortgage_interest_rate,
            price_to_rent_coeff,
            avg_price_sqm,
            cadastral_value_coefficient,
            avg_invest_return,
            buying_from_individual,
            tax_deduction
        )
        
    def analyze(self):
        self._comparator.calculate_purchasing_expenses()
        self._comparator.calculate_renting_expenses()
        self._comparator.which_convenient()
        
        return {
            "answer": {
                "Purchasing": {
                    "purchase_price": self._comparator.purchase_price,
                    "price_evaluation": self._comparator.is_fair_price(),
                    "fair_price": self._comparator.fair_price,
                    "mortgage_fee": self._comparator.mortgage_fee,
                    "condo_owner_fee": self._comparator.condo_owner_fees,
                    "renovation": self._comparator.renovation,
                    "purchasing_expenses": self._comparator.purchasing_expenses,
                    "investments_returns": self._comparator.investments_returns,
                    "total_net_flow": self._comparator.yearly_purchasing_expenses,
                },
                "Renting": {
                    "fair_rent": self._comparator.fair_rent,
                    "yearly_fair_rent": self._comparator.yearly_rent,
                    "tax_deduction": self._comparator.tax_deduction,
                    "investments_returns": self._comparator.investments_returns,
                    "total_net_flow": self._comparator.yearly_renting_expenses,
                },
                "Summary": {
                    "convenience": self._comparator.convenience["What's convenient?"],
                    "saving": self._comparator.convenience["How much saving?"]
                }
            }
    }  
