function update(progress){

}

function draw(){

}

function updateAudio(){}

function progressKeyEvents(){}

function loop(timestamp){
  var progress = timestamp - lastRender

  update(progress)
  draw()

  lastRender = timestamp
  window.requestAnimationFrame(loop)
}

var lastRender = 0;
window.requestAnimationFrame(loop)
