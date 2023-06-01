def add_data_function():  
  from .models import Layer1, Layer2, Account

  if not Layer1.objects.exists():
    Layer1_data = [
            {
                "id": "1",
                "name": "Current Asset",
                "main_layer": "assets",
                "keyword": "#current_asset"
            },
            {
                "id": "2",
                "name": "Direct Expense",
                "main_layer": "expense",
                "keyword": "#direct_expense"
            },
            {
                "id": "3",
                "name": "Current Laibility",
                "main_layer": "laibility",
                "keyword": "#current_laibility"
            },
            {
                "id": "4",
                "name": "Direct Revenue",
                "main_layer": "revenue",
                "keyword": "#direct_revenue"
            },
            {
                "id": "5",
                "name": "Owner Equity",
                "main_layer": "equity",
                "keyword": "#owner_equity"
            }
        ]

    for data in Layer1_data:
        layer1 = Layer1(**data)
        layer1.save()
        
        
        
  if not Layer2.objects.exists():
    Layer2_data = [
            {
                "id": "1",
                "name": "Cash in Hand",
                "layer1_id": "1",
                "main_layer": "assets",
                "keyword": "#cash_hand_asset"
            },
            {
                "id": "2",
                "name": "Receivable",
                "layer1_id": "1",
                "main_layer": "assets",
                "keyword": "#receivable_asset"
            },
            {
                "id": "3",
                "name": "Bank",
                "layer1_id": "1",
                "main_layer": "assets",
                "keyword": "#fixed_asset"
            },
            {
                "id": "4",
                "name": "Inventory",
                "layer1_id": "1",
                "main_layer": "assets",
                "keyword": "#inventory_asset"
            },
            {
                "id": "5",
                "name": "Salaries, Wages & Benefits",
                "layer1_id": "2",
                "main_layer": "expense",
                "keyword": "#SWB_expense"
            },
            {
                "id": "6",
                "name": "Direct Expense",
                "layer1_id": "2",
                "main_layer": "expense",
                "keyword": "#directex_expense"
            },
            {
                "id": "7",
                "name": "Marketing & Advertisment",
                "layer1_id": "2",
                "main_layer": "expense",
                "keyword": "#MA_expense"
            },
            {
                "id": "8",
                "name": "Supplier",
                "layer1_id": "3",
                "main_layer": "laibility",
                "keyword": "#supplier_laibility"
            },
            {
                "id": "9",
                "name": "Sale",
                "layer1_id": "4",
                "main_layer": "revenue",
                "keyword": "#cash_sale_revenue"
            },
            {
                "id": "10",
                "name": "Capital Investment",
                "layer1_id": "5",
                "main_layer": "equity",
                "keyword": "#CI_equity"
            },
        ]

    for data in Layer2_data:
        layer2 = Layer2(**data)
        layer2.save()
        
        

  if not Account.objects.exists():
    account_data = [
              {
                "id": "1",
                "title": "Cash in Hand",
                "layer1_id": "1",
                "layer2_id": "1",
                "main_layer": "assets",
                "keyword": "#cashInhand"
              },
              {
                "id": "2",
                "title": "Inventory",
                "layer1_id": "1",
                "layer2_id": "4",
                "main_layer": "assets",
                "keyword": "#Inventory"
              },
              {
                "id": "3",
                "title": "Cost of Goods Sold",
                "layer1_id": "2",
                "layer2_id": "6",
                "main_layer": "expense",
                "keyword": "#Costofgoodssold"
              },
              {
                "id": "4",
                "title": "Cash Sale",
                "layer1_id": "4",
                "layer2_id": "9",
                "main_layer": "revenue",
                "keyword": "#cash_sale"
              },
              {
                "id": "5",
                "title": "Investment",
                "layer1_id": "5",
                "layer2_id": "10",
                "main_layer": "equity",
                "keyword": "#investment"
              }
        ]

    for data in account_data:
         account = Account(**data)
         account.save()