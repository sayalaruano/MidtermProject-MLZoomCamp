#%%
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from padelpy import padeldescriptor
from sklearn.feature_selection import VarianceThreshold
import requests

url = 'http://localhost:9696/predict'

molecule_id = 'CHEMBL179256'

canonical_smile = 'OC(=O)c1ccc2c(c1)nc(c3ccc(O)cc3F)n2C4CCCCC4'

molecule = {"Canonical_smile": canonical_smile, 
            "Chembl_id": molecule_id}

molecule_df = pd.DataFrame(molecule, index=[0])

molecule_df.to_csv('molecule_test.smi', sep='\t', index=False, header=False)

fingerprint_outfile = 'CDK_example_testing.csv'

fingerprint_descriptorfile = 'Data/MolFingerprints/Fingerprinter.xml'

padeldescriptor(mol_dir='molecule_test.smi', 
                d_file=fingerprint_outfile,
                descriptortypes= fingerprint_descriptorfile,
                detectaromaticity=True,
                standardizenitro=True,
                standardizetautomers=True,
                threads=2,
                removesalt=True,
                log=True,
                fingerprints=True)

cdk_molecule_df = pd.read_csv("CDK_example_testing.csv") 

low_var_feat_names = pd.read_csv("low_var_feat_names.csv")

## Obtain feature matrix with low variance features 
cdk_low_var = cdk_molecule_df.drop('Name', axis=1)
cdk_low_var = cdk_molecule_df[low_var_feat_names["Descriptor_Name"].values]
#%%

cdk_molecule_json = cdk_low_var.to_json(orient="records")
#%%

cdk_mol_json_test = {"FP1":1,"FP2":1,"FP5":1,"FP7":1,"FP9":0,"FP12":0,"FP13":1,"FP14":1,"FP15":0,"FP16":1,"FP17":0,"FP19":0,"FP22":0,"FP23":0,"FP24":1,"FP25":0,"FP26":0,"FP28":0,"FP30":0,"FP31":1,"FP32":0,"FP34":1,"FP35":0,"FP37":1,"FP38":0,"FP41":0,"FP42":0,"FP43":0,"FP44":0,"FP45":0,"FP48":0,"FP49":1,"FP50":1,"FP51":1,"FP53":0,"FP55":0,"FP56":1,"FP57":0,"FP60":0,"FP63":1,"FP64":1,"FP66":1,"FP67":1,"FP68":1,"FP69":1,"FP70":1,"FP71":1,"FP72":1,"FP73":0,"FP74":0,"FP75":0,"FP76":1,"FP77":0,"FP78":0,"FP79":0,"FP80":1,"FP82":0,"FP86":0,"FP88":0,"FP89":0,"FP90":0,"FP91":0,"FP93":0,"FP94":0,"FP95":0,"FP98":1,"FP101":1,"FP102":1,"FP103":1,"FP104":0,"FP105":0,"FP106":1,"FP107":0,"FP108":0,"FP109":0,"FP110":0,"FP112":1,"FP113":1,"FP114":0,"FP115":1,"FP116":1,"FP118":1,"FP119":1,"FP120":1,"FP121":1,"FP123":1,"FP124":1,"FP125":0,"FP126":1,"FP127":1,"FP128":1,"FP129":0,"FP130":0,"FP131":0,"FP132":1,"FP133":1,"FP134":0,"FP135":1,"FP137":1,"FP138":1,"FP139":0,"FP140":0,"FP141":0,"FP142":0,"FP144":1,"FP145":0,"FP146":0,"FP148":1,"FP149":1,"FP152":0,"FP153":1,"FP156":0,"FP157":1,"FP158":0,"FP160":0,"FP161":0,"FP163":0,"FP164":0,"FP165":1,"FP166":1,"FP167":0,"FP170":0,"FP171":1,"FP172":1,"FP173":0,"FP174":1,"FP175":1,"FP176":1,"FP178":1,"FP179":1,"FP180":1,"FP182":0,"FP184":1,"FP185":0,"FP186":0,"FP187":1,"FP189":1,"FP191":1,"FP192":0,"FP193":1,"FP194":0,"FP195":1,"FP196":0,"FP197":0,"FP198":0,"FP199":1,"FP200":1,"FP201":0,"FP203":1,"FP204":1,"FP205":1,"FP206":1,"FP208":1,"FP209":1,"FP210":0,"FP211":0,"FP215":1,"FP216":1,"FP219":1,"FP221":0,"FP222":1,"FP223":1,"FP224":0,"FP225":1,"FP226":1,"FP227":0,"FP228":1,"FP229":1,"FP230":0,"FP234":0,"FP235":0,"FP236":0,"FP237":0,"FP238":0,"FP240":1,"FP241":0,"FP242":1,"FP244":1,"FP247":1,"FP249":0,"FP250":0,"FP255":0,"FP256":0,"FP257":1,"FP259":0,"FP260":1,"FP263":1,"FP264":0,"FP265":1,"FP266":0,"FP268":1,"FP269":1,"FP271":1,"FP273":1,"FP274":0,"FP275":0,"FP276":1,"FP282":0,"FP283":1,"FP284":1,"FP285":1,"FP286":1,"FP287":1,"FP289":0,"FP291":0,"FP293":0,"FP294":1,"FP295":0,"FP297":1,"FP298":0,"FP301":1,"FP302":1,"FP304":0,"FP305":1,"FP306":1,"FP307":1,"FP308":1,"FP309":0,"FP310":0,"FP311":0,"FP313":0,"FP317":0,"FP318":1,"FP319":0,"FP320":0,"FP323":1,"FP324":0,"FP325":1,"FP326":1,"FP327":0,"FP331":0,"FP334":0,"FP335":0,"FP336":0,"FP337":1,"FP338":0,"FP340":1,"FP341":1,"FP343":0,"FP344":0,"FP345":0,"FP347":1,"FP350":0,"FP352":1,"FP353":1,"FP354":0,"FP355":1,"FP359":0,"FP360":1,"FP361":0,"FP362":0,"FP363":1,"FP364":0,"FP365":1,"FP366":1,"FP367":0,"FP368":1,"FP369":0,"FP370":0,"FP371":0,"FP373":0,"FP374":1,"FP375":1,"FP376":1,"FP377":0,"FP379":0,"FP380":0,"FP381":0,"FP383":0,"FP384":0,"FP385":1,"FP387":1,"FP388":0,"FP389":0,"FP390":1,"FP394":0,"FP395":0,"FP399":0,"FP400":0,"FP401":0,"FP402":0,"FP403":0,"FP404":1,"FP405":0,"FP406":0,"FP408":0,"FP409":1,"FP410":0,"FP411":0,"FP413":0,"FP414":0,"FP415":0,"FP416":0,"FP417":0,"FP419":1,"FP420":0,"FP421":0,"FP422":0,"FP423":0,"FP425":0,"FP426":0,"FP427":0,"FP430":0,"FP431":0,"FP433":0,"FP436":1,"FP437":1,"FP438":0,"FP439":0,"FP440":0,"FP442":0,"FP443":0,"FP444":0,"FP447":0,"FP448":1,"FP450":0,"FP451":0,"FP452":1,"FP453":0,"FP455":1,"FP456":0,"FP457":0,"FP459":0,"FP460":1,"FP461":0,"FP462":1,"FP463":0,"FP464":0,"FP465":0,"FP466":0,"FP470":0,"FP471":0,"FP472":0,"FP474":0,"FP475":0,"FP476":1,"FP477":0,"FP478":0,"FP481":1,"FP483":1,"FP484":0,"FP486":0,"FP487":0,"FP488":1,"FP489":0,"FP491":1,"FP492":1,"FP493":0,"FP494":0,"FP496":1,"FP497":1,"FP498":0,"FP499":1,"FP500":0,"FP501":1,"FP502":1,"FP503":0,"FP504":0,"FP505":1,"FP506":1,"FP509":1,"FP511":1,"FP512":0,"FP513":0,"FP514":0,"FP515":0,"FP517":1,"FP518":1,"FP521":0,"FP524":1,"FP525":0,"FP527":0,"FP528":1,"FP529":0,"FP531":0,"FP532":0,"FP533":1,"FP534":0,"FP535":0,"FP536":1,"FP539":0,"FP545":0,"FP546":0,"FP547":1,"FP548":1,"FP549":0,"FP550":0,"FP554":1,"FP555":0,"FP559":0,"FP560":0,"FP561":0,"FP562":0,"FP563":0,"FP564":1,"FP565":0,"FP566":1,"FP568":1,"FP569":0,"FP570":0,"FP571":0,"FP572":0,"FP576":1,"FP577":1,"FP579":0,"FP580":0,"FP581":0,"FP582":1,"FP584":1,"FP586":0,"FP587":0,"FP588":0,"FP592":0,"FP593":0,"FP594":0,"FP597":1,"FP598":0,"FP599":0,"FP600":1,"FP601":0,"FP602":0,"FP604":0,"FP606":0,"FP611":0,"FP612":1,"FP613":0,"FP614":1,"FP615":0,"FP616":0,"FP617":0,"FP618":1,"FP619":1,"FP620":1,"FP621":0,"FP622":0,"FP623":0,"FP624":0,"FP626":1,"FP627":0,"FP632":1,"FP633":0,"FP634":0,"FP636":0,"FP637":1,"FP639":1,"FP640":0,"FP643":0,"FP644":1,"FP645":0,"FP646":0,"FP647":1,"FP648":0,"FP649":0,"FP651":1,"FP654":0,"FP655":1,"FP656":0,"FP657":0,"FP658":0,"FP659":0,"FP660":0,"FP661":0,"FP662":0,"FP663":0,"FP665":0,"FP666":1,"FP667":0,"FP668":0,"FP670":0,"FP674":1,"FP675":0,"FP676":0,"FP677":0,"FP678":0,"FP680":0,"FP681":1,"FP684":0,"FP685":0,"FP686":0,"FP687":1,"FP688":0,"FP690":0,"FP691":0,"FP692":1,"FP694":0,"FP696":1,"FP698":0,"FP700":1,"FP701":0,"FP702":1,"FP703":0,"FP704":0,"FP707":1,"FP708":0,"FP709":0,"FP712":1,"FP713":1,"FP714":0,"FP715":1,"FP716":0,"FP717":0,"FP718":1,"FP719":1,"FP720":1,"FP721":1,"FP723":0,"FP724":0,"FP726":0,"FP728":0,"FP729":0,"FP733":1,"FP734":0,"FP735":0,"FP736":1,"FP737":1,"FP738":0,"FP739":0,"FP740":1,"FP741":0,"FP744":0,"FP745":0,"FP746":1,"FP748":0,"FP749":1,"FP750":0,"FP751":0,"FP753":1,"FP754":0,"FP756":0,"FP757":0,"FP759":0,"FP760":0,"FP761":0,"FP762":0,"FP763":0,"FP764":1,"FP765":1,"FP766":1,"FP767":0,"FP770":0,"FP771":0,"FP772":0,"FP773":1,"FP774":1,"FP775":0,"FP776":0,"FP777":1,"FP778":0,"FP779":1,"FP780":1,"FP781":1,"FP783":0,"FP784":0,"FP786":0,"FP787":1,"FP788":0,"FP790":0,"FP791":0,"FP793":1,"FP795":0,"FP796":1,"FP797":0,"FP798":0,"FP799":0,"FP800":0,"FP801":0,"FP805":1,"FP806":0,"FP807":1,"FP808":0,"FP809":1,"FP810":0,"FP811":0,"FP813":0,"FP817":0,"FP818":0,"FP819":0,"FP820":0,"FP824":0,"FP825":0,"FP827":0,"FP829":0,"FP830":0,"FP831":1,"FP832":1,"FP833":0,"FP835":1,"FP836":0,"FP837":0,"FP838":0,"FP839":0,"FP840":0,"FP841":1,"FP842":0,"FP843":0,"FP844":1,"FP845":0,"FP846":0,"FP847":1,"FP849":0,"FP851":0,"FP852":0,"FP853":1,"FP855":0,"FP859":0,"FP860":0,"FP862":1,"FP864":0,"FP867":0,"FP868":0,"FP869":0,"FP870":1,"FP873":0,"FP874":0,"FP876":0,"FP877":0,"FP878":1,"FP879":1,"FP880":0,"FP881":0,"FP882":0,"FP883":0,"FP884":1,"FP886":1,"FP887":0,"FP888":0,"FP892":0,"FP893":0,"FP895":0,"FP896":0,"FP897":0,"FP898":1,"FP899":0,"FP900":0,"FP904":1,"FP905":1,"FP908":0,"FP909":0,"FP910":1,"FP911":0,"FP912":1,"FP915":0,"FP916":0,"FP917":1,"FP918":0,"FP920":1,"FP922":1,"FP923":0,"FP924":0,"FP930":1,"FP931":1,"FP932":1,"FP933":1,"FP934":1,"FP935":0,"FP936":0,"FP938":0,"FP941":1,"FP942":0,"FP943":0,"FP944":1,"FP945":1,"FP946":0,"FP947":0,"FP948":0,"FP949":0,"FP950":0,"FP951":1,"FP955":1,"FP956":0,"FP957":0,"FP958":0,"FP959":1,"FP960":0,"FP961":0,"FP962":1,"FP963":0,"FP964":0,"FP965":0,"FP966":0,"FP967":0,"FP968":0,"FP969":0,"FP970":1,"FP971":0,"FP974":1,"FP975":0,"FP976":0,"FP977":0,"FP978":0,"FP979":0,"FP980":0,"FP981":1,"FP983":0,"FP984":1,"FP985":1,"FP986":1,"FP987":0,"FP988":1,"FP989":0,"FP990":1,"FP992":0,"FP993":0,"FP994":1,"FP995":0,"FP997":0,"FP998":0,"FP999":0,"FP1001":1,"FP1002":0,"FP1003":0,"FP1004":0,"FP1005":0,"FP1006":0,"FP1007":1,"FP1008":0,"FP1009":0,"FP1011":1,"FP1012":0,"FP1015":0,"FP1016":0,"FP1017":0,"FP1018":0,"FP1019":0,"FP1022":0}

#%%
response = requests.post(url, json=cdk_molecule_json).json()
print(response)

if response['Active'] == True:
    print('Molecule %s is active against betalactamases' % molecule_id)
else:
    print('Molecule %s is not active against betalactamases' % molecule_id)

#%%