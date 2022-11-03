
/**
 * 
 * @param {*} numberToInspect
 * @param {*} divider
 * @param {Number}
 */
export function getNearMultiple(numberToInspect, divider) {
    const remainder = numberToInspect % divider;
    return remainder !== 0
        ? ((divider - remainder)) + numberToInspect
        : numberToInspect;
}
