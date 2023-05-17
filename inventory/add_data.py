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
                "name": "Non-Current Asset",
                "main_layer": "assets",
                "keyword": "#non_current_asset"
            },
            {
                "id": "3",
                "name": "Direct Expense",
                "main_layer": "expense",
                "keyword": "#direct_expense"
            },
            {
                "id": "4",
                "name": "Indirect Expense",
                "main_layer": "expense",
                "keyword": "#indirect_expense"
            },
            {
                "id": "5",
                "name": "Owner Equity",
                "main_layer": "equity",
                "keyword": "#owner_equity"
            },
            {
                "id": "6",
                "name": "Current Laibility",
                "main_layer": "laibility",
                "keyword": "#current_laibility"
            },
            {
                "id": "7",
                "name": "Non-Current Laibility",
                "main_layer": "laibility",
                "keyword": "#non_current_laibility"
            },
            {
                "id": "8",
                "name": "Direct Revenue",
                "main_layer": "revenue",
                "keyword": "#direct_revenue"
            },
            {
                "id": "9",
                "name": "Indirect Revenue",
                "main_layer": "revenue",
                "keyword": "#indirect_revenue"
            }
        ]

    for data in Layer1_data:
        layer1 = Layer1(**data)
        layer1.save()
        
        
        
  if not Layer2.objects.exists():
    Layer2_data = [
            {
                "id": "1",
                "name": "Cash & Bank",
                "layer1_id": "1",
                "main_layer": "assets",
                "keyword": "#cash_bank_asset"
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
                "name": "Fixed Assets",
                "layer1_id": "2",
                "main_layer": "assets",
                "keyword": "#fixed_asset"
            },
            {
                "id": "4",
                "name": "Inventory",
                "layer1_id": "2",
                "main_layer": "assets",
                "keyword": "#inventory_asset"
            },
            {
                "id": "5",
                "name": "Salaries, Wages & Benefits",
                "layer1_id": "3",
                "main_layer": "expense",
                "keyword": "#SWB_expense"
            },
            {
                "id": "6",
                "name": "Entertaiment",
                "layer1_id": "3",
                "main_layer": "expense",
                "keyword": "#entertaiment_expense"
            },
            {
                "id": "7",
                "name": "Direct Expense",
                "layer1_id": "3",
                "main_layer": "expense",
                "keyword": "#directex_expense"
            },
            {
                "id": "8",
                "name": "Marketing & Advertisment",
                "layer1_id": "3",
                "main_layer": "expense",
                "keyword": "#MA_expense"
            },
            {
                "id": "9",
                "name": "Donation & Charity",
                "layer1_id": "4",
                "main_layer": "expense",
                "keyword": "#DC_expense"
            },
            {
                "id": "10",
                "name": "Other Expense",
                "layer1_id": "4",
                "main_layer": "expense",
                "keyword": "#other_expense"
            },
            {
                "id": "11",
                "name": "Capital Investment",
                "layer1_id": "5",
                "main_layer": "equity",
                "keyword": "#CI_equity"
            },
            {
                "id": "12",
                "name": "Supplier",
                "layer1_id": "6",
                "main_layer": "laibility",
                "keyword": "#supplier_laibility"
            },
            {
                "id": "13",
                "name": "Bank Loan",
                "layer1_id": "7",
                "main_layer": "laibility",
                "keyword": "#Bank_loan_laibility"
            },
            {
                "id": "14",
                "name": "Cash Sale",
                "layer1_id": "8",
                "main_layer": "revenue",
                "keyword": "#cash_sale_revenue"
            },
            {
                "id": "15",
                "name": "Installment Sale",
                "layer1_id": "8",
                "main_layer": "revenue",
                "keyword": "#installment_sale_revenue"
            },
            {
                "id": "16",
                "name": "Other Income",
                "layer1_id": "9",
                "main_layer": "revenue",
                "keyword": "#other_income_revenue"
            },
            {
                "id": "17",
                "name": "Processing Fee",
                "layer1_id": "9",
                "main_layer": "revenue",
                "keyword": "#processing_fee_revenue"
            }
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
                "layer1_id": "2",
                "layer2_id": "4",
                "main_layer": "assets",
                "keyword": "#Inventory"
              },
              {
                "id": "3",
                "title": "Receivable",
                "layer1_id": "1",
                "layer2_id": "2",
                "main_layer": "assets",
                "keyword": "#SalariesWagesBenefits"
              },
              {
                "id": "4",
                "title": "Salaries, Wages & Benefits",
                "layer1_id": "3",
                "layer2_id": "5",
                "main_layer": "expense",
                "keyword": "#SalariesWagesBenefits"
              },
              {
                "id": "5",
                "title": "Direct Expense",
                "layer1_id": "3",
                "layer2_id": "7",
                "main_layer": "expense",
                "keyword": "#SalariesWagesBenefits"
              },
              {
                "id": "6",
                "title": "Marketing & Advertisment",
                "layer1_id": "3",
                "layer2_id": "8",
                "main_layer": "expense",
                "keyword": "#MA_expense"
              },
              {
                "id": "7",
                "title": "Supplier",
                "layer1_id": "6",
                "layer2_id": "12",
                "main_layer": "laibility",
                "keyword": "#supplier_laibility"
              },
              {
                "id": "8",
                "title": "Cash Sale",
                "layer1_id": "8",
                "layer2_id": "14",
                "main_layer": "revenue",
                "keyword": "#cash_sale"
              },
              {
                "id": "9",
                "title": "Equity",
                "layer1_id": "5",
                "layer2_id": "11",
                "main_layer": "equity",
                "keyword": "#equity"
              }
        ]

    for data in account_data:
         account = Account(**data)
         account.save()