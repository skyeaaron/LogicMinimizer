from pyeda.inter import expr, espresso_exprs

rule = '(b | c | d | e | f | g | h | i | j | ba | bb | bc | bd | be | bf | bg | bh) & (bi | bj | ca | cb | cc | cd | ce | cf | cg | ch | ci | cj | da | db | dc | dd | de) & ((bi & df & dg & dh & di) | (bj & dj & ea & eb & ec) | (ca & ed & ee & ef & eg) | (cb & eh & ei & ej & fa) | (cc & fb & fc & fd & fe) | (cd & ff & fg & fh & fi) | (ce & fj & ga & gb & gc) | (cf & gd & ge & gf & gg) | (cg & gh & gi & gj & ha) | (ch & hb & hc & hd & he) | (ci & hf & hg & hh & hi) | (cj & hj & ia & ib & ic) | (da & id & ie & if & ig) | (db & ih & ii & ij & ja) | (dc & jb & jc & jd & je) | (dd & jf & jg & jh & ji) | (de & jj & baa & bab & bac))'
#rule = 'b | a'
f1 = expr(rule)
dnf_form = f1.to_dnf()
print('in dnf form. trying to minimize.')
f1_min, = espresso_exprs(dnf_form)
print(f1_min)