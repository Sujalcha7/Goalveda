
def display_transactions(connection, user_id):
    st.title("Transaction")

    st.header("All Transactions")
    recent_expenses, all_expenses, recent_income, all_income, total_expense, total_income, total_remaining = get_transaction_history(connection, user_id)
    # all_transactions = all_expenses + all_income
    st.subheader("expenses")
    data_lists_recent_expense = []  # Initialize an empty list
    
    for expense in all_expenses:
        # Extracting the necessary elements for display
        data_lists_recent_expense.append((expense[1], expense[2], expense[3], expense[5]))

    # Creating  DataFrame with the selected columns
    df_e = pd.DataFrame(data_lists_recent_expense, columns=['Category', 'name', 'Amount', 'Transaction_Time'])
    st.table(df_e)

    st.header('Income')
    data_lists_recent_income=[]
    for income in all_income:
        # Extracting the necessary elements for display
        data_lists_recent_income.append((income[1], income[2], income[4]))

    # Creating  DataFrame with the selected columns
    df_r_i = pd.DataFrame(data_lists_recent_income, columns=[ 'name', 'Amount', 'Transaction_Time'])
    st.table(df_r_i)