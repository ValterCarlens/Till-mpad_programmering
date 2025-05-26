namespace Slutprojekt
{
    /// <summary>
    /// Här är min klass
    /// </summary>
    public class Budget
    {
        /// <summary>
        /// Namnet på budgeten
        /// </summary>
        public string Name { get; set; }
        public string Description { get; set; }
        public int Income { get; set; }
        public int Expenditure { get; set; }
        public int Leftover { get; set; }
        public string SavingGoal { get; set; }
    }
}