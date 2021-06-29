
proof1 = r'''
    1 + 1 = 2
    '''
proof2 = r'''
    let \varepsilon > 0 
    if | x - 3 | < \delta = \varepsilon / 2
    then 2 * | x - 3 | < \varepsilon
    then | 2 * x - 6 | < \varepsilon
    then 2 * x \rightarrow 6 as x \rightarrow 3
    '''