"""Data profiling helpers. Pure pandas, easy to unit-test."""
import numpy as np
import pandas as pd


def _num(v):
    """Convert numpy scalars to plain Python floats/ints for JSON."""
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return None if np.isnan(v) else round(float(v), 4)
    return v


def profile_dataframe(df: pd.DataFrame, name: str = 'data.csv') -> dict:
    profile = {
        'name': name,
        'rows': int(len(df)),
        'columns_count': int(df.shape[1]),
        'columns': [],
        'numeric_summary': [],
        'correlations': [],
        'preview': df.head(10).astype(str).values.tolist(),
        'headers': [str(c) for c in df.columns],
    }

    for col in df.columns:
        s = df[col]
        info = {
            'name': str(col),
            'dtype': str(s.dtype),
            'missing': int(s.isna().sum()),
            'missing_pct': round(100 * s.isna().mean(), 1),
            'unique': int(s.nunique()),
        }
        if pd.api.types.is_numeric_dtype(s):
            info['kind'] = 'numeric'
        elif pd.api.types.is_datetime64_any_dtype(s):
            info['kind'] = 'datetime'
        else:
            info['kind'] = 'text'
            top = s.value_counts().head(5)
            info['top_values'] = [{'value': str(k), 'count': int(v)} for k, v in top.items()]
        profile['columns'].append(info)

    numeric = df.select_dtypes(include='number')
    for col in numeric.columns:
        s = numeric[col].dropna()
        if s.empty:
            continue
        profile['numeric_summary'].append({
            'column': str(col),
            'mean': _num(s.mean()), 'median': _num(s.median()),
            'std': _num(s.std()), 'min': _num(s.min()), 'max': _num(s.max()),
        })

    if numeric.shape[1] >= 2:
        corr = numeric.corr().round(3)
        for i, c1 in enumerate(corr.columns):
            for c2 in corr.columns[i + 1:]:
                v = corr.loc[c1, c2]
                if not np.isnan(v):
                    profile['correlations'].append({'a': str(c1), 'b': str(c2), 'r': float(v)})
        profile['correlations'].sort(key=lambda x: -abs(x['r']))

    return profile
