import unittest
import pandas as pd
import re

OUTPUT_DIR = 'data/output/OutputBasemodel.csv' # Adjust path before running

def whitespace_remover(dataframe):

    # iterating over the columns
    for i in dataframe.columns:

        # checking datatype of each columns
        if dataframe[i].dtype == 'object':

            # applying strip function on column
            dataframe[i] = dataframe[i].map(str.strip)
        else:

            # if condn. is False then it will do nothing.
            pass

df=pd.read_csv(OUTPUT_DIR, delimiter=";", skiprows= 2)
whitespace_remover(df)
df.columns = [col.strip() for col in df.columns]

susc_pop_pattern = r"^S\d{4}" 
exp_pop_pattern = r"^E\d{4}" 
infc_pop_pattern = r"^I\d{4}" 
recv_pop_pattern = r"^R\d{4}" 

pop_pattern = r"^[SEIR]\d{4}" 

# Test the sum of SEIR for all ticks is constant for each population category 
class TestConsSEIR(unittest.TestCase): 

    # Defining the population categories
    @classmethod
    def setUpClass(cls):
        cls.pop_categories = sorted(set(col[1:] for col in df.columns if re.match(pop_pattern, col)))
        cls.pop_seir_columns = sorted(set(col[0] for col in df.columns if re.match(pop_pattern, col)))

    def test_cons_seir_pop_category(self):
        for cat in self.pop_categories: 
            required_cols = [f"S{cat}", f"E{cat}", f"I{cat}", f"R{cat}"]
            
            if all(col in df.columns for col in required_cols):
                seir_sum = df[f"S{cat}"] + df[f"E{cat}"] + df[f"I{cat}"] + df[f"R{cat}"]
                
                # The sum of seir for the pop_cat is constant, i.e. only has one value
                pop_is_constant = seir_sum.nunique() == 10
        
                self.assertTrue(
                    pop_is_constant, 
                    f"Sum of SEIR population for population group {cat} has different values.")

            else:
                missing = [col for col in required_cols if col not in df.columns]
                print(f"Skipping test for constant pop for pop category {cat}. Missing columns {missing}")
                continue
        

# Test that population values are not negative
class TestNonNegSEIR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s_cols = [col for col in df.columns if re.match(susc_pop_pattern, col)]
        cls.e_cols = [col for col in df.columns if re.match(exp_pop_pattern, col)]
        cls.i_cols = [col for col in df.columns if re.match(infc_pop_pattern, col)]
        cls.r_cols = [col for col in df.columns if re.match(recv_pop_pattern, col)]

    def test_non_neg_susceptible(self):
        for col in self.s_cols:
            is_pop_non_neg = (df[col] >= 0).all()
            self.assertTrue(is_pop_non_neg, f"{col} column has negative values.")
            
    def test_non_neg_exposed(self):
        for col in self.e_cols:
            is_pop_non_neg = (df[col] >= 0).all()
            self.assertTrue(is_pop_non_neg, f"{col} column has negative values.")
        
    def test_non_neg_infected(self):
        for col in self.i_cols:
            is_pop_non_neg = (df[col] >= 0).all()
            self.assertTrue(is_pop_non_neg, f"{col} column has negative values.")
    
    def test_non_neg_recovered(self):
        for col in self.r_cols:
            is_pop_non_neg = (df[col] >= 0).all()
            self.assertTrue(is_pop_non_neg, f"{col} column has negative values.")
  

if __name__ == "__main__":
    unittest.main()