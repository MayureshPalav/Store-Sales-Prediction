const nav_icon = document.getElementById('nav-icon');
const nav_section = document.getElementById('nav-section');

nav_icon.addEventListener('click',()=>{
    nav_section.classList.toggle('nav-active');
})

// Navbar 
const nav_items  = document.querySelectorAll('.nav-items li');
console.log(nav_items);

if(window.location.pathname === '/prediction'){
    let result = document.createElement('a');
    result.setAttribute('href','#result');
    result.textContent = "RESULT"

    nav_items[0].replaceChild(result,nav_items[0].firstElementChild);

    let info = document.createElement('a');
    info.setAttribute('href','#info');
    info.textContent = "INFO"

    nav_items[1].replaceChild(info,nav_items[1].firstElementChild);
    
    let predict = document.createElement('a');
    predict.setAttribute('href','#prediction');
    predict.textContent = "REPORT"

    nav_items[2].replaceChild(predict,nav_items[2].firstElementChild);
    
}

// Prediction
const growth_values=document.querySelectorAll('.growth')
console.log(growth_values);

const growth_colors=['#237A10','#268719','#299322','#2DA02B','#30AC34','#33B93D','#36C646','#39D24F','#3DDF58','#40EB61','#43F86A']

growth_values.forEach((value,index)=>{
    value.style.background = growth_colors[index];
    console.log("Applied");
})

const fall_values=document.querySelectorAll('.fall')

const fall_colors = ['#6C0000','#7B0707','#890E0E','#981414','#A71B1B','#B62222','#C42929','#D33030','#E23636','#F03D3D','#FF4444']
fall_values.forEach((value,index)=>{
    value.style.background = fall_colors[index];
    console.log("Applied");
})