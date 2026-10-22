#!/usr/bin/env python3
"""Multi-sport odds value scanner. Standard library only; never places bets."""
import argparse,csv,datetime as dt,json,math,sqlite3,statistics
from pathlib import Path

def fair_probs(odds):
    inv=[1/x for x in odds]
    s=sum(inv)
    return [x/s for x in inv],s-1

def score(row, min_edge, min_ev):
    try:
        odds=float(row['odds']); p=float(row['model_probability']); uncertainty=float(row.get('uncertainty',0.05) or 0.05)
        if not (1.01<=odds<=1000 and 0<p<1 and 0<=uncertainty<1): raise ValueError('invalid probability, odds or uncertainty')
        lower=max(0,p-1.28*uncertainty)
        ev=p*odds-1; conservative=lower*odds-1
        edge=p-1/odds
        if edge<min_edge or conservative<min_ev: return None
        return {'sport':row['sport'],'event':row['event'],'market':row['market'],'selection':row['selection'], 'odds':odds,'p_model':round(p,4),'p_lower':round(lower,4),'edge':round(edge,4),'ev':round(ev,4),'conservative_ev':round(conservative,4),'source':row.get('source',''),'timestamp':row.get('timestamp','')}
    except (ValueError,KeyError,TypeError):return None

def main():
    a=argparse.ArgumentParser(description='Analyse des cotes multisports (sans pari automatique)')
    a.add_argument('csv_file');a.add_argument('--db',default='historique.sqlite');a.add_argument('--min-edge',type=float,default=0.03);a.add_argument('--min-conservative-ev',type=float,default=0.02)
    args=a.parse_args()
    with open(args.csv_file,encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    picks=[x for r in rows if (x:=score(r,args.min_edge,args.min_conservative_ev))]
    picks.sort(key=lambda x:x['conservative_ev'],reverse=True)
    db=sqlite3.connect(args.db)
    db.execute('CREATE TABLE IF NOT EXISTS analyses (id INTEGER PRIMARY KEY, analyzed_at TEXT, sport TEXT, event TEXT, market TEXT, selection TEXT, odds REAL, p_model REAL, p_lower REAL, edge REAL, ev REAL, conservative_ev REAL, source TEXT, timestamp TEXT)')
    for x in picks: db.execute('INSERT INTO analyses (analyzed_at,sport,event,market,selection,odds,p_model,p_lower,edge,ev,conservative_ev,source,timestamp) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',(dt.datetime.now(dt.timezone.utc).isoformat(),*[x[k] for k in ('sport','event','market','selection','odds','p_model','p_lower','edge','ev','conservative_ev','source','timestamp')]))
    db.commit();db.close()
    print(json.dumps({'analyzed':len(rows),'shortlisted':len(picks),'candidates':picks[:20], 'warning':'Les probabilités doivent provenir d’un modèle validé hors échantillon. Aucune rentabilité garantie. Aucun pari placé.'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
