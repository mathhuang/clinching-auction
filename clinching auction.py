import pandas as pd

# 初始化表格中的数据
bid_data = {
    "Bidder": ["A", "B", "C", "D", "E"],
    "Marginal Value (1 unit)": [123, 75, 125, 85, 45],
    "Marginal Value (2 units)": [113, 5, 125, 65, 25],
    "Marginal Value (3 units)": [103, 3, 49, 7, 5]
}

# 将数据转换为 DataFrame
df = pd.DataFrame(bid_data).set_index("Bidder")

# 总供应数量
total_supply = 5
price_levels = sorted(set(df.values.flatten()))  # 从低到高排序所有边际价值

# 执行 clinching 拍卖
def clinching_auction(df, total_supply, price_levels):
    # 初始化结果存储
    results = {bidder: {"Units Won": 0, "Payments": []} for bidder in df.index}
    allocated_number = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
    # 遍历每个价格水平
    for price in price_levels:
        # 1. 即时更新每个竞标者的需求（在价格达到边际价值时减少）
        demand = {bidder: sum(1 for val in df.loc[bidder] if val > price) for bidder in df.index}
        for bidder in demand:
            demand[bidder] -= allocated_number[bidder]

        # 输出当前价格和需求
        print(f"\n--- Price: {price} ---")
        print(f"Current Demand: {demand}")
        
        # 2. 检查哪些竞标者符合 clinching 条件，并记录符合条件的竞标者
        clinched_bidders = []
        
        print(f"total_supply: {total_supply}")
        
        for bidder in df.index:
            # 计算去掉当前竞标者后的其他竞标者的需求总和
            others_demand = sum(demand[other_bidder] for other_bidder in df.index if other_bidder != bidder)
            
            # 输出调试信息：去掉该竞标者后的其他竞标者的需求总和
            print(f"Bidder {bidder} - Others' Demand Sum: {others_demand}")
            
            # 如果其他竞标者的需求总和小于剩余供应量，则当前竞标者可以 clinch
            if others_demand < total_supply:
                clinched_units = total_supply - others_demand
                clinched_bidders.append((bidder, clinched_units))
                print(f"--> Bidder {bidder} clinches {clinched_units} unit(s) at price {price}")

        # 3. 为所有符合条件的竞标者分配物品，并在分配后更新需求
        for bidder, clinched_units in clinched_bidders:
            results[bidder]["Units Won"] += clinched_units
            results[bidder]["Payments"].extend([price] * clinched_units)
            
            # 更新需求：需求在被分配了一个单位后也应减少
            allocated_number[bidder] += clinched_units
            print(f"Allocated {clinched_units} units to Bidder {bidder}. New Demand: {demand[bidder]}")

        # 4. 更新总供应量
        total_supply -= sum(units for _, units in clinched_bidders)
        
        # 输出调试信息：分配后的总供应量
        print(f"Remaining Supply after allocation: {total_supply}")
        print("-" * 40)

        # 如果供应已经分配完毕，提前结束
        if total_supply <= 0:
            break

    # 5. 计算每个竞标者的总支付
    for bidder in results:
        results[bidder]["Total Payment"] = sum(results[bidder]["Payments"])

    return pd.DataFrame(results).T

# 运行拍卖并输出结果
auction_results = clinching_auction(df, total_supply, price_levels)
print(auction_results)
