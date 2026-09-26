from expense_splitter import Expense, balances


def test_balances_for_a_single_shared_expense():
    dinner = Expense("ann", 900, ("ann", "bob", "cy"), "dinner")
    assert balances([dinner]) == {"ann": 600, "bob": -300, "cy": -300}


def test_balances_accumulate_across_expenses():
    expenses = [
        Expense("ann", 600, ("ann", "bob")),
        Expense("bob", 200, ("ann", "bob")),
    ]
    assert balances(expenses) == {"ann": 200, "bob": -200}
