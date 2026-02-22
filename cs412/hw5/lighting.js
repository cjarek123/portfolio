function hexToRGB(hex){
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  return [r, g, b];
}

const ambientSlider = document.getElementById("slider-ka");
const ambientDisplay = document.getElementById("slider-ka-value");
const ambientColor = document.getElementById("colorSelectorAmbient");
const diffuseSlider = document.getElementById("slider-kd");
const diffuseDisplay = document.getElementById("slider-kd-value");
const diffuseColor = document.getElementById("colorSelectorDiffuse");
const specularSlider = document.getElementById("slider-ks");
const specularDisplay = document.getElementById("slider-ks-value");
const specularColor = document.getElementById("colorSelectorSpecular");
const shininessSlider = document.getElementById('slider-s');
const shininessDisplay = document.getElementById('slider-s-value');
const backgroundColor = document.getElementById('colorSelector');
const lightPositionX = document.getElementById("slider-x");
const lightXDisplay = document.getElementById("slider-x-value");
const lightPositionY = document.getElementById("slider-y");
const lightYDisplay = document.getElementById("slider-y-value");
const lightPositionZ = document.getElementById("slider-z");
const lightZDisplay = document.getElementById("slider-z-value");
const modeSelection = document.getElementById("select_id");

function updateAmbientReflection(){
  ambientDisplay.textContent = ambientSlider.value;
  gl.uniform1f(uKa, parseFloat(ambientSlider.value));
}
function updateAmbientColor(){
  const color = hexToRGB(ambientColor.value);
  gl.uniform3f(uAmbientColor, color[0], color[1], color[2]);
}
function updateDiffuseReflection(){
  diffuseDisplay.textContent = diffuseSlider.value;
  gl.uniform1f(uKd, parseFloat(diffuseSlider.value));
}
function updateDiffuseColor(){
  const color = hexToRGB(diffuseColor.value);
  gl.uniform3f(uDiffuseColor, color[0], color[1], color[2]);
}
function updateSpecularReflection(){
  specularDisplay.textContent = specularSlider.value;
  gl.uniform1f(uKs, parseFloat(specularSlider.value));
}
function updateSpecularColor(){
  const color = hexToRGB(specularColor.value);
  gl.uniform3f(uSpecularColor, color[0], color[1], color[2]);
}
function updateShininess(){
  shininessDisplay.textContent = shininessSlider.value;
  gl.uniform1f(uShininess, parseFloat(shininessSlider.value));
}
function updateBackgroundColor(){
  //update background color
}
function updateLightPosition(){
  lightXDisplay.textContent = lightPositionX.value;
  lightYDisplay.textContent = lightPositionY.value;
  lightZDisplay.textContent = lightPositionZ.value;
  gl.uniform3f(uLightPos,
    parseFloat(lightPositionX.value),
    parseFloat(lightPositionY.value),
    parseFloat(lightPositionZ.value));
}
function updateMode(){
  const mode = parseInt(modeSelection.value);
  gl.uniform1i(uMode, mode);
}
function updateAllLightingUniforms(){
    updateAmbientReflection();
    updateAmbientColor();
    updateDiffuseReflection();
    updateDiffuseColor();
    updateSpecularReflection();
    updateSpecularColor();
    updateShininess();
    updateBackgroundColor();
    updateLightPosition();
    updateMode();
}

ambientSlider.addEventListener("input", updateAmbientReflection);
ambientColor.addEventListener("input", updateAmbientColor);
diffuseSlider.addEventListener("input", updateDiffuseReflection);
diffuseColor.addEventListener("input", updateDiffuseColor);
specularSlider.addEventListener("input", updateSpecularReflection);
specularColor.addEventListener("input", updateSpecularColor);
shininessSlider.addEventListener("input", updateShininess);
backgroundColor.addEventListener("input", updateBackgroundColor);
lightPositionX.addEventListener("input", updateLightPosition);
lightPositionY.addEventListener("input", updateLightPosition);
lightPositionZ.addEventListener("input", updateLightPosition);
modeSelection.addEventListener("change", updateMode);