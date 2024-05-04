from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config

@dataclass
class Transaction(DataClassJsonMixin):
    description: str
    date_sold: str
    date_acquired: str
    sales_proceeds: str
    cost_or_other_basis: str
    adjustment_amount: str
    is_wash_sale: bool = field(metadata=config(exclude=lambda x: True))
    reporting_category: str
    long_short: str
    wash_sale: str = field(init=False)
    gain_loss: str = field(init=False)
    
    def __post_init__(self):
        self.sales_proceeds = self.sales_proceeds.replace(",", "") # change "1,000" to "1000"
        self.cost_or_other_basis = self.cost_or_other_basis.replace(",", "") # change "1,000" to "1000"
        self.gain_loss = "0" if self.is_wash_sale else str(round(float(self.sales_proceeds) - float(self.cost_or_other_basis), 2))
        self.wash_sale = "Yes" if self.is_wash_sale else None