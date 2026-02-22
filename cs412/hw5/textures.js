function loadTexture(gl, url){
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);

    const level = 0;
    const internalFormat = gl.RGBA;
    const srcFormat = gl.RGBA;
    const srcType = gl.UNSIGNED_BYTE;
    
    // Create a checkerboard texture (no file needed, no CORS issues)
    const checkerboard = createCheckerboardTexture(64);
    
    gl.texImage2D(
        gl.TEXTURE_2D,
        level,
        internalFormat,
        64,
        64,
        0,
        srcFormat,
        srcType,
        checkerboard
    );

    // Set texture parameters
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    
    console.log("Texture loaded: procedural checkerboard (64x64)");
    return texture;
}

function createCheckerboardTexture(size){
    const data = new Uint8Array(size * size * 4);
    let index = 0;
    
    for(let i = 0; i < size; i++){
        for(let j = 0; j < size; j++){
            // Check if square is in checkerboard pattern
            const isWhite = ((Math.floor(i / 8) + Math.floor(j / 8)) % 2) === 0;
            const color = isWhite ? 255 : 50;
            
            data[index++] = color;     // R
            data[index++] = color;     // G
            data[index++] = color;     // B
            data[index++] = 255;       // A
        }
    }
    
    return data;
}

function isPowerOf2(value){
    return (value&(value-1)) === 0;
}

function setTextureAttribute(gl, buffers, programInfo){
    const num = 2;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 0;
    const offset = 0;

    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.textureCoord);
    gl.vertexAttribPointer(
        programInfo.attribLocations.textureCoord,
        num,
        type,
        normalize,
        stride,
        offset)
        ;
    
        gl.enableVertexAttribArray(programInfo.attribLocations.textureCoord);
}