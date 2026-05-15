import pandas as pd


class SaaSEconomicsModel:
    """
    A class to simulate the financial performance of a SaaS business.
    Calculates key metrics like Active Users, Revenue, and Cumulative Profit.
    """

    def __init__(self,
                 months: int = 24,
                 fixed_costs: float = 10000.0,  # Monthly salaries, rent, etc.
                 new_users_per_month: int = 500,  # Monthly acquisition target
                 price: float = 50.0,  # Subscription price
                 cac: float = 40.0,  # Customer Acquisition Cost
                 churn_rate: float = 0.10,  # Monthly churn (10%)
                 arpu_variable_cost: float = 2.0  # Support and transaction costs per user
                 ):
        self.months = months
        self.fixed_costs = fixed_costs
        self.new_users_per_month = new_users_per_month
        self.price = price
        self.cac = cac
        self.churn_rate = churn_rate
        self.arpu_variable_cost = arpu_variable_cost

    def calculate_simulation(self) -> pd.DataFrame:
        """Runs a step-by-step monthly simulation of the business model."""
        months_list = list(range(1, self.months + 1))
        active_users = []
        current_active = 0

        revenue = []
        marketing_costs = []
        variable_costs = []

        for m in months_list:
            # Calculate churned and new users
            lost = int(current_active * self.churn_rate)
            new = self.new_users_per_month
            current_active = current_active - lost + new

            active_users.append(current_active)
            revenue.append(current_active * self.price)
            marketing_costs.append(new * self.cac)
            variable_costs.append(current_active * self.arpu_variable_cost)

        df = pd.DataFrame({
            'Month': months_list,
            'Active_Users': active_users,
            'Revenue': revenue,
            'Marketing_Costs': marketing_costs,
            'Variable_Costs': variable_costs,
            'Fixed_Costs': [self.fixed_costs] * self.months
        })

        # Financial Calculations
        df['Total_Costs'] = df['Marketing_Costs'] + df['Variable_Costs'] + df['Fixed_Costs']
        df['Monthly_Profit'] = df['Revenue'] - df['Total_Costs']
        df['Cumulative_Profit'] = df['Monthly_Profit'].cumsum()

        return df