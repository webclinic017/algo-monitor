export default class BetterCast {
    private constructor() {}
    
    static cast(value) : BetterType {
        if (BetterCast.isString(value)) {
            return 'string';
        }
        else if (BetterCast.isNumber(value)) {
            return 'number';
        }
        else if (BetterCast.isArray(value)) {
            return 'array';
        }
        else if (BetterCast.isFunction(value)) {
            return 'function';
        }
        else if (BetterCast.isObject(value)) {
            return 'object';
        }
        else if (BetterCast.isClass(value)) {
            return 'class';
        }
        else if (BetterCast.isNull(value)) {
            return 'null';
        }
        else if (BetterCast.isUndefined(value)) {
            return 'undefined';
        }
        else if (BetterCast.isBoolean(value)) {
            return 'boolean';
        }
        else if (BetterCast.isRegExp(value)) {
            return 'regexp';
        }
        else if (BetterCast.isError(value)) {
            return 'error';
        }
        else if (BetterCast.isDate(value)) {
            return 'date';
        }
        else if (BetterCast.isSymbol(value)) {
            return 'symbol';
        }
        else {
            throw 'Unexpected Type';
        }
    }

    
    static isString (value) {
        return typeof value === 'string' || value instanceof String;
    }
    
    static isNumber (value) {
        return typeof value === 'number' && isFinite(value);
    }
    
    static isArray (value) {
        return value && typeof value === 'object' && value.constructor === Array;
    }
    
    static isFunction (value) {
        return typeof value === 'function';
    }
    
    static isObject (value) {
        return value && typeof value === 'object' && value.constructor === Object;
    }
    
    static isClass (value) {
        return value && typeof value === 'object' && value.constructor === Function;
    }
    
    static isNull (value) {
        return value === null;
    }		
    
    static isUndefined (value) {
        return typeof value === 'undefined';
    }
    
    static isBoolean (value) {
        return typeof value === 'boolean';
    }
    
    static isRegExp (value) {
        return value && typeof value === 'object' && value.constructor === RegExp;
    }
    
    static isError (value) {
        return value instanceof Error && typeof value.message !== 'undefined';
    }
    
    static isDate (value) {
        return value instanceof Date;
    }
    
    static isSymbol (value) {
        return typeof value === 'symbol';
    }
}

export type BetterType = 'string' | 'number' | 'array' | 'function' | 'object' | 'class' | 'null' | 'undefined' | 'boolean' | 'regexp' | 'error' | 'date' | 'symbol';