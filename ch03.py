# 3.1 Calculate daily volatility
def getDailyVol(close, span0=100):
  df0 = close.index.searchsorted(close.index-pd.Timedelta(days=1))
  df0 = df0[df0>0]
  df0 = pd.Series(close.index[df0-1], index=close.index[close.shape[0]-df0.shape[0]:])
  df0 = close.loc[df0.index]/close.loc[df0.values].values-1
  df0 = df0.ewm(span=span0).std()
  return df0

# 3.2 triple-barrier labeling
def applyPtSlonT1(close, events, ptsl, molecule):
  # t1 : vertical barrier
  # pt : upper horizontal barrier
  # sl : lower horizontal barrier

  events_ = evnets.loc[molecule]
  out = events_[['t1]].copy(deep=True)
  
  if ptsl[0]>0: pt=ptsl[0]*events_['trgt']
  else: pt = pd.Series(index=events.index) # NaNs
  if ptsl[1]>0: sl=-ptsl[1]*events_['trgt']
  else: sl = pd.Series(index=events.index) # NaNs
  
  for loc,t1 in events_['t1'].fillna(close.index[-1]).iteritems():
    df0 = close[loc:t1] # price path
    df0 = (df0/close[loc]-1)*events_.at[loc, 'side']
    out.loc[loc, 'sl'] = df0[df0<sl[loc]].index.min()
    out.loc[loc, 'pt'] = df0[df0>pt[loc]].index.min()
    
  return out
