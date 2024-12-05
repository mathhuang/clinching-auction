import pandas as pd

bid_data = {
    "Bidder": ["A", "B", "C", "D", "E"],
    "Marginal Value (1 unit)": [123, 75, 125, 85, 45],
    "Marginal Value (2 units)": [113, 5, 125, 65, 25],
    "Marginal Value (3 units)": [103, 3, 49, 7, 5]
}

df = pd.DataFrame(bid_data).set_index("Bidder")

total_supply = 5
price_levels = sorted(set(df.values.flatten())) 

def clinching_auction(df, total_supply, price_levels):
    results = {bidder: {"Units Won": 0, "Payments": []} for bidder in df.index}
    allocated_number = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}

    for price in price_levels:
        demand = {bidder: sum(1 for val in df.loc[bidder] if val > price) for bidder in df.index}
        for bidder in demand:
            demand[bidder] -= allocated_number[bidder]

        print(f"\n--- Price: {price} ---")
        print(f"Current Demand: {demand}")
        
        clinched_bidders = []
        
        print(f"total_supply: {total_supply}")
        
        for bidder in df.index:
            others_demand = sum(demand[other_bidder] for other_bidder in df.index if other_bidder != bidder)
            
            print(f"Bidder {bidder} - Others' Demand Sum: {others_demand}")

            if others_demand < total_supply:
                clinched_units = total_supply - others_demand
                clinched_bidders.append((bidder, clinched_units))
                print(f"--> Bidder {bidder} clinches {clinched_units} unit(s) at price {price}")

        for bidder, clinched_units in clinched_bidders:
            results[bidder]["Units Won"] += clinched_units
            results[bidder]["Payments"].extend([price] * clinched_units)
            
            allocated_number[bidder] += clinched_units
            print(f"Allocated {clinched_units} units to Bidder {bidder}. New Demand: {demand[bidder]}")

        total_supply -= sum(units for _, units in clinched_bidders)
        
        print(f"Remaining Supply after allocation: {total_supply}")
        print("-" * 40)

        if total_supply <= 0:
            break

    for bidder in results:
        results[bidder]["Total Payment"] = sum(results[bidder]["Payments"])

    return pd.DataFrame(results).T

auction_results = clinching_auction(df, total_supply, price_levels)
print(auction_results)
