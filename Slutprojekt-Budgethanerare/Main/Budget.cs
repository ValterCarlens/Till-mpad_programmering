public class Budget
{
    public string Name { get; }
    public DateTime CreationDate { get; }
    public decimal Income { get; }
    public decimal Expenses { get; }
    public decimal Outcome => Income - Expenses; // Read-only, calculated property

    public Budget(string name, DateTime creationDate, decimal income, decimal expenses)
    {
        Name = name;
        CreationDate = creationDate;
        Income = income;
        Expenses = expenses;
    }
}