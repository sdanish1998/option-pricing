# Author: Danish Shah (sdanish1998@gmail.com)
# Created: 10-05-2022
# Last update: 11-02-2022

class SimpleBinomialModel:
    
    # Initialize an option
    def __init__(self, stock_price, strike_price, maturity=1, up=1.05, down=0.95, rate=0.0):
        """
        @param: stock_price     Initial stock price at t=0
        @param: strike_price    Strike price of call option
        @param: maturity        Number of periods
        @param: up              One-timestep fractional increase in price
        @param: down            One-timestep fractional decrease in price
        @param: rate            Interest rate of bond
        """
        self.S0 = stock_price
        self.K = strike_price
        self.N = maturity
        self.u = up
        self.d = down
        self.r = rate
        self.pi = self.calculate_pi()

    # Risk-neutral probability
    def calculate_pi(self):
        return ((1 + self.r) - self.d)/(self.u - self.d)

    # Price (pay-off) of the option
    def option_price(self, Xu, Xd):
        # Option price at time t is the discounted 
        # average price at time t+1
        return (self.pi*Xu + (1 - self.pi)*Xd)/(1 + self.r)

    # Hedging ratio (delta)
    def stock_position(self, Xu, Xd, S):
        return (Xu - Xd)/(S*(self.u - self.d))

    # Money market ratio (eta)
    def bond_position(self, Xu, Xd, S):
        return (self.u*Xd - self.d*Xu)/((self.u - self.d)*(1 + self.r))
        
    def run_multiperiod_model(self):
        """
        @returns S      Possible stock prices for all time periods
        @returns X      Option prices for all time periods
        @returns delta  Hedging ratio for all time periods
        @returns eta    Bond ratio for all time periods
        """
        S, X, delta, eta = [], [], [], []
        ST, XT = [], []
        for i in range(N+1):
            Si = S0 * (self.u**(self.N-i)) * (self.d**i)
            ST.append(Si)
            XT.append(max(Si-self.K, 0))
        S.append(ST)
        X.append(XT)

        t = self.N-1
        while (t >= 0):
            St, Xt, delta_t, eta_t = [], [], [], []
        
            for i in range(t+1):
                St.append(ST[i]/self.u)
                Xt.append(option_price(XT[i], XT[i+1]))
                delta_t.append(stock_position(XT[i], XT[i+1], ST[i]/self.u))
                eta_t.append(bond_position(XT[i], XT[i+1], ST[i]/self.u))
        
            S.insert(0, St)
            X.insert(0, Xt)
            delta.insert(0, delta_t)
            eta.insert(0, eta_t)

            ST, XT = St, Xt
            t -= 1

        return S, X, delta, eta