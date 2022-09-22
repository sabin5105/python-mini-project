import os
import pandas as pd

output_md = ""
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
score = pd.read_csv(PATH+'/data/class_score_en.csv').rename(columns={"# midterm (max 125)":"Midterm", " final (max 100)":"Final"})
score['total'] = (40 / 125) * score['Midterm'] + (60 / 100) * score['Final']

def get_arithmetics(s : pd.Series) -> pd.Series:
    return pd.Series([s.mean(), s.var(), s.median(), s.min(), s.max()], index=['Mean', 'Variance', 'Median', 'Min', 'Max'])


output_md += "# **Individual Score** \n"
output_md += score.to_markdown()
output_md += '\n'
output_md += "# **Examination Analysis** \n"

for exam in score.columns:
    output_md += f"* {exam} \n"
    arithmetics = get_arithmetics(score[exam])
    output_md += f"    * Mean: {arithmetics['Mean']:.3f} \n"
    output_md += f"    * Variance: {arithmetics['Variance']:.3f} \n"
    output_md += f"    * Median: {arithmetics['Median']:.3f} \n"
    output_md += f"    * Min/Max: ({arithmetics['Min']:.3f}, {arithmetics['Max']}) \n"

with open(PATH+"/output/score_analysis.md", 'a+') as f:
    f.write(output_md)