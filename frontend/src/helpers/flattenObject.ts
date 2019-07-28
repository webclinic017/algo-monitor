export default class FlattenObject {
    private constructor() {}

    static flatten(obj, separator = '.') {
        var newObj = {};
        this.dive("", obj, newObj, separator);
        return newObj;
    }

    private static dive(currentKey, into, target, separator) {
        for (var i in into) {
            if (into.hasOwnProperty(i)) {
                var newKey = i;
                var newVal = into[i];
                
                if (currentKey.length > 0) {
                    newKey = currentKey + separator + i;
                }
                
                if (typeof newVal === "object") {
                    this.dive(newKey, newVal, target, separator);
                } else {
                    target[newKey] = newVal;
                }
            }
        }
    }
}