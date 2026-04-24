from src.config import (RVB_CALC_CPY_CDT_TAX, RVB_CALC_CPY_MTG_TAX,
                        RVB_CALC_CPY_REG_TAX, RVB_CALC_CPY_VAT,
                        RVB_CALC_INDIV_CDT_TAX, RVB_CALC_INDIV_MTG_TAX,
                        RVB_CALC_INDIV_OTH_TAX, RVB_CALC_INDIV_REG_TAX,
                        RVB_CALC_MIN_TAX)


class Comparator:
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
        tax_deduction: float = 0.0,
    ):

        self.purchase_price = purchase_price
        self.sqm = sqm
        self.condo_owner_fees_coeff = condo_owner_fees_coeff
        self.notary_fees = notary_fees
        self.payback_years = payback_years
        self.years_occurring_renovation = years_occurring_renovation
        self.mortgage_interest_rate = mortgage_interest_rate
        self.price_to_rent_coeff = price_to_rent_coeff
        self.avg_price_sqm = avg_price_sqm
        self.cadastral_value_coefficient = cadastral_value_coefficient
        self.avg_invest_return = avg_invest_return
        self.buying_from_individual = buying_from_individual
        self.tax_deduction = tax_deduction

        self.cadastral_value = purchase_price / cadastral_value_coefficient
        self.investments_returns = purchase_price * avg_invest_return

    def calculate_purchasing_expenses(self):

        # Estimate condo fees
        self.condo_owner_fees = -(self.cadastral_value * self.condo_owner_fees_coeff)

        # Dilute 1/3 of the value of the property over the years between each renovation
        self.renovation = -(self.cadastral_value / 3) / self.years_occurring_renovation

        #  Taxes change according to the nature of the vendor
        if self.buying_from_individual == "Privato":
            registry_tax = RVB_CALC_INDIV_REG_TAX * self.cadastral_value
            mortgage_tax = RVB_CALC_INDIV_MTG_TAX
            cadastral_tax = RVB_CALC_INDIV_CDT_TAX
            other_expenses = RVB_CALC_INDIV_OTH_TAX
            self.taxes = registry_tax + mortgage_tax + cadastral_tax + other_expenses

        elif self.buying_from_individual == "Azienda":
            vat = RVB_CALC_CPY_VAT * self.purchase_price
            registry_tax = RVB_CALC_CPY_REG_TAX
            mortgage_tax = RVB_CALC_CPY_MTG_TAX
            cadastral_tax = RVB_CALC_CPY_CDT_TAX
            self.taxes = vat + registry_tax + mortgage_tax + cadastral_tax

        # Taxes are at least 1000€ + notary fees, diluted in the payback years
        self.purchasing_expenses = (
            -(max(RVB_CALC_MIN_TAX, self.taxes) + self.notary_fees) / self.payback_years
        )

        # Calculate mortage fee
        self.mortgage_fee = -(self.purchase_price * self.mortgage_interest_rate)

        self.yearly_purchasing_expenses = (
            self.condo_owner_fees
            + self.renovation
            + self.purchasing_expenses
            + self.investments_returns
            + self.mortgage_fee
        )

    def calculate_renting_expenses(self):
        self.fair_rent = self.purchase_price * self.price_to_rent_coeff
        self.yearly_rent = -(self.fair_rent * 12)
        self.yearly_renting_expenses = (
            self.yearly_rent + self.investments_returns + self.tax_deduction
        )

    def which_convenient(self):
        self.convenience = {}
        self.convenience["What's convenient?"] = "buying" if self.yearly_renting_expenses > self.yearly_purchasing_expenses else "renting"
        self.convenience["How much saving?"] = abs(self.yearly_renting_expenses - self.yearly_purchasing_expenses)
        
    def is_fair_price(self) -> str:

        self.fair_price = self.avg_price_sqm * self.sqm
        if self.purchase_price > self.fair_price:
            return "high"
        elif self.purchase_price == self.fair_price:
            return "fair"
        else:
            return "low"