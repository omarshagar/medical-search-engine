// =====================================================================================================

function setScale(scale) {
    
    if (ref_screen == null) return scale;

    return ref_screen.rescale(scale);
}

// ====================================================================================================

function setFontScale(scale) {
    
    if (ref_screen == null) return scale;

    return ref_screen.fontRescale(scale);
}

// ====================================================================================================

function unscale(scale) {
    
    if (ref_screen == null) return scale;

    return ref_screen.rescaleInverse(scale);
}

// ====================================================================================================
