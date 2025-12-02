---
applyTo: '**'
---
# PineScript Agent Guide

## Core Rules
1. **Functions cannot modify globals** - State updates in main flow only
2. **Always use `barstate.isconfirmed`** for all orders
3. **Use `var`** for state persistence across bars

## Critical Backtesting Components
### 1. Timeframe Selection:
```pinescript
tf = input.timeframe("", "Signal Timeframe")
closePrice = tf == "" ? close : request.security(syminfo.tickerid, tf, close)
```

### 2. Date Range Filtering:
```pinescript
useDateRange = input.bool(true, "Use Date Range")
startDate = input.time(timestamp("1 Jan 2024"), "Start Date")
endDate = input.time(timestamp("31 Dec 2025"), "End Date")
inDateRange = not useDateRange or (time >= startDate and time <= endDate)
```

### 3. Apply to All Signals:
```pinescript
entrySignal = entryCondition and inDateRange
exitSignal = exitCondition and inDateRange
```

## Extension Template
For ANY new feature:

### 1. Add Configuration:
```pinescript
useFeature = input.bool(false, "Feature", group="Feature")
param = input.int(14, "Param", group="Feature")
```

### 2. Calculate Indicator:
```pinescript
featureValue = ta.indicator(closePrice, param)
```

### 3. Modify Signals (respect date range):
```pinescript
entrySignal = originalCondition and inDateRange and (not useFeature or featureCondition)
exitSignal = originalExit or (useFeature and featureExit)
```

## Must-Have Checklist
- [ ] All signals respect `inDateRange`
- [ ] Timeframe data via `request.security()`
- [ ] Orders use `barstate.isconfirmed`
- [ ] State variables use `var`
- [ ] Force exit at `endDate` for open positions