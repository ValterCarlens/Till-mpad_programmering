public class Program
{
    private static List<Budget> budgets = new List<Budget>();

    public static void Main(string[] args)
    {

        LoadBudgetsFromFile(); // Load budgets from file at startup

        bool running = true;

        while (running)
        {
            Console.WriteLine("---BudgethanteringProgram---");
            Console.WriteLine("1. Skapa ny budget");
            Console.WriteLine("2. Välj budget befintlig budget");
            Console.WriteLine("3. Avsluta programmet");
            Console.Write("Välj ett alternativ: ");
            string choice = Console.ReadLine();

            switch (choice)
            {
                case "1":
                    CreateBudget();
                    break;
                case "2":
                    SelectBudget();
                    break;
                case "3":
                    running = false;
                    break;
                default:
                    Console.WriteLine("Ogiltigt alternativ. Försök igen.");
                    break;
            }
        }
    }

    private static void CreateBudget()
    {
        Console.Write("Ange namn på budget: ");
        string name = Console.ReadLine();
        DateTime creationDate = DateTime.Now;

        decimal income;
        while (true)
        {
            Console.Write("Ange total inkomst: ");
            if (decimal.TryParse(Console.ReadLine(), out income))
                break;
            Console.WriteLine("Ogiltig inkomst. Försök igen.");
        }

        decimal expenses;
        while (true)
        {
            Console.Write("Ange totala utgifter: ");
            if (decimal.TryParse(Console.ReadLine(), out expenses))
                break;
            Console.WriteLine("Ogiltiga utgifter. Försök igen.");
        }

        Budget newBudget = new Budget(name, creationDate, income, expenses);

        budgets.Add(newBudget);
        Console.WriteLine($"Budget '{name}' skapades");

        SaveBudgetsToFile(); 
    }

    private static void SelectBudget()
    {
        if (budgets.Count == 0)
        {
            Console.WriteLine("Inget budget existerar, skapa en ny först.");
            Thread.Sleep(4000); 
            return;
        }

        Console.WriteLine("Välj befintlig budget:");
        for (int i = 0; i < budgets.Count; i++)
        {
            Console.WriteLine($"{i + 1}. {budgets[i].Name}");
        }
        Console.Write("Ange numret på budgeten du vill välja: ");
        int index = int.Parse(Console.ReadLine()) - 1;

        if (index >= 0 && index < budgets.Count)
        {
            Budget selectedBudget = budgets[index];
            Console.WriteLine($"Vald budget: {selectedBudget.Name}");
            Console.WriteLine($"Datum skapad: {selectedBudget.CreationDate}");
            Console.WriteLine($"Inkomst: {selectedBudget.Income}");
            Console.WriteLine($"Utgifter: {selectedBudget.Expenses}");
            Console.WriteLine($"Pengar kvar: {selectedBudget.Outcome}");
        }
        else
        {
            Console.WriteLine("Ogiltigt alternativ.");
        }
    }
    private static void SaveBudgetsToFile()
{
    string filePath = "budgets.json";
    string json = System.Text.Json.JsonSerializer.Serialize(budgets);
    File.WriteAllText(filePath, json);
    Console.WriteLine("Budgets saved to file.");
}

    private static void LoadBudgetsFromFile()
    {
        string filePath = "budgets.json";
        if (File.Exists(filePath))
        {
            string json = File.ReadAllText(filePath);
            budgets = System.Text.Json.JsonSerializer.Deserialize<List<Budget>>(json);
            Console.WriteLine("Budgets loaded from file.");
        }
        else
        {
            Console.WriteLine("No saved budgets found.");
        }
    }
    
}