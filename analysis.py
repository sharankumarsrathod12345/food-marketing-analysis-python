from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
# Resolve inputs relative to this script, regardless of the caller's directory.
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
pd.set_option('display.max_columns', 12)
pd.set_option('display.float_format', lambda value: f'{value:,.3f}')
plt.rcParams.update({'figure.figsize': (10, 5), 'font.size': 11,
                     'axes.spines.top': False, 'axes.spines.right': False})
BLUE = '#24577A'


source = ROOT / 'data' / 'cleaned_ufood_marketing.csv'
if not source.exists():
    raise FileNotFoundError(f'Place the supplied cleaned CSV at {source}')
cleaned_reference = pd.read_csv(source)
raw = pd.read_csv(ROOT / 'data' / 'u_food_marketing.csv')
food = raw.drop_duplicates().reset_index(drop=True).copy()
shared = sorted(set(food.columns) & set(cleaned_reference.columns))
pd.testing.assert_frame_equal(food[shared], cleaned_reference[shared].reset_index(drop=True))
sensitivity = pd.DataFrame({
    'population':['all source rows','exact duplicates removed'],
    'rows':[len(raw),len(food)],
    'last_campaign_responses':[int(raw.Response.sum()),int(food.Response.sum())],
    'response_rate':[raw.Response.mean(),food.Response.mean()]})
display(sensitivity)
sensitivity.to_csv(OUT / 'duplicate_sensitivity.csv',index=False)
prior = [f'AcceptedCmp{i}' for i in range(1, 6)]
channels = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
marital = [c for c in food if c.startswith('marital_')]
education = [c for c in food if c.startswith('education_')]
required = prior + channels + ['Response','Age','Kidhome','Teenhome','MntTotal',
    'MntWines','MntFruits','MntMeatProducts','MntFishProducts','MntSweetProducts','MntGoldProds']
assert not (set(required) - set(food)), 'Required columns are missing'
assert len(food) > 0 and marital and education
assert food[required + marital + education].notna().all().all(), 'Investigate missing inputs'
assert food[prior + ['Response'] + marital + education].isin([0, 1]).all().all()
assert food[marital].sum(axis=1).eq(1).all(), 'Marital indicators must be one-hot'
assert food[education].sum(axis=1).eq(1).all(), 'Education indicators must be one-hot'
assert food[channels + ['Kidhome','Teenhome','MntTotal']].ge(0).all().all()
assert food['Age'].between(0, 120).all()
spend_columns = ['MntWines','MntFruits','MntMeatProducts','MntFishProducts','MntSweetProducts']
assert food[spend_columns].sum(axis=1).eq(food['MntTotal']).all(), 'Spend definition changed'
quality = pd.DataFrame({'check':['rows','columns','exact duplicate rows','missing cells'],
                        'value':[len(food),len(food.columns),food.duplicated().sum(),food.isna().sum().sum()]})
display(quality)
quality.to_csv(OUT / 'quality_checks.csv', index=False)


food = food.copy()
food['children_at_home'] = food['Kidhome'] + food['Teenhome']
food['prior_campaign_acceptances'] = food[prior].sum(axis=1)
food['any_campaign_accepted'] = food[prior + ['Response']].max(axis=1)
food['marital_status'] = food[marital].idxmax(axis=1).str.removeprefix('marital_')
food['education_level'] = food[education].idxmax(axis=1).str.removeprefix('education_')
food['age_group'] = pd.cut(food['Age'], [-np.inf,30,40,50,60,70,np.inf],
                           labels=['30 or younger','31–40','41–50','51–60','61–70','71 or older'])
summary = pd.Series({'profile_rows':len(food),'response_count':int(food['Response'].sum()),
    'response_rate':food['Response'].mean(),'any_acceptance_count':int(food['any_campaign_accepted'].sum()),
    'any_acceptance_rate':food['any_campaign_accepted'].mean()})
display(summary.to_frame('value'))
summary.to_csv(OUT / 'summary.csv')


def segment_table(column):
    result = food.groupby(column, observed=True).agg(
        profiles=('Response','size'), responses=('Response','sum'),
        response_rate=('Response','mean'), any_acceptance_rate=('any_campaign_accepted','mean'),
        median_food_spend=('MntTotal','median'), total_food_spend=('MntTotal','sum'))
    result['profile_share'] = result['profiles'] / len(food)
    assert result['profiles'].sum() == len(food)
    assert result['responses'].sum() == food['Response'].sum()
    return result
age = segment_table('age_group')
children = segment_table('children_at_home')
marital_summary = segment_table('marital_status')
education_summary = segment_table('education_level')
for name, table in [('age',age),('children',children),('marital',marital_summary),('education',education_summary)]:
    table.to_csv(OUT / f'{name}_segments.csv')
display(age)
display(children)


fig, axes = plt.subplots(1,2,figsize=(13,5))
age['profiles'].plot.barh(ax=axes[0], color=BLUE)
axes[0].set(title='Age distribution', xlabel='Customer-profile rows', ylabel='Age group')
(age['response_rate']*100).plot.barh(ax=axes[1], color=BLUE)
axes[1].set(title='Response rate within each age group', xlabel='Response = 1 / segment rows (%)', ylabel='')
axes[1].set_xlim(0, max(40,age['response_rate'].max()*130))
for i, (_,row) in enumerate(age.iterrows()):
    axes[1].text(row['response_rate']*100+0.7,i,f"n={int(row['profiles']):,}",va='center')
fig.suptitle('Supplied cleaned extract • n=2,021 • observation period unspecified')
fig.tight_layout(); fig.savefig(OUT/'age_response.png',dpi=160,bbox_inches='tight'); plt.show()


fig, axes = plt.subplots(1,2,figsize=(12,4.5))
(children['response_rate']*100).plot.bar(ax=axes[0],color=BLUE,rot=0)
axes[0].set(title='Response by children at home',xlabel='Children at home',ylabel='Within-group response (%)')
children['median_food_spend'].plot.bar(ax=axes[1],color=BLUE,rot=0)
axes[1].set(title='Median recorded food spending',xlabel='Children at home',ylabel='Source monetary units')
fig.tight_layout(); fig.savefig(OUT/'children_response_spend.png',dpi=160,bbox_inches='tight'); plt.show()


display(marital_summary)
display(education_summary)


channel_counts = food[channels].sum().rename(index={
    'NumWebPurchases':'Web','NumCatalogPurchases':'Catalogue','NumStorePurchases':'Store'})
channel_counts.to_csv(OUT/'channel_purchase_counts.csv',header=['recorded_purchases'])
fig,ax=plt.subplots(figsize=(9,4.5))
channel_counts.sort_values().plot.barh(ax=ax,color=BLUE)
ax.set(title='Recorded purchases by channel',xlabel='Purchase count—not revenue',ylabel='')
fig.tight_layout();fig.savefig(OUT/'channel_purchases.png',dpi=160,bbox_inches='tight');plt.show()


spend_cutoff = food['MntTotal'].median()
food['behavior_segment'] = np.select([
    food['MntTotal'].ge(spend_cutoff) & food['Recency'].le(30),
    food['MntTotal'].ge(spend_cutoff) & food['Recency'].gt(30),
    food['MntTotal'].lt(spend_cutoff) & food['Recency'].le(30)],
    ['Higher spend / recent','Higher spend / less recent','Lower spend / recent'],
    default='Lower spend / less recent')
behavior = segment_table('behavior_segment')
print(f'Spending cutoff: {spend_cutoff:,.0f} source monetary units; recency cutoff: 30 days')
display(behavior)
behavior.to_csv(OUT/'behavior_segments.csv')
fig,ax=plt.subplots(figsize=(10,5))
(behavior['response_rate']*100).sort_values().plot.barh(ax=ax,color=BLUE)
ax.set(title='Last-campaign response by behavioral segment',xlabel='Within-segment response (%)',ylabel='')
fig.tight_layout();fig.savefig(OUT/'behavior_segments.png',dpi=160,bbox_inches='tight');plt.show()
