const loader = document.querySelector('.loader');
const content = document.querySelector('.homeContent');
const nav = document.querySelector('.navbar1');
//page loader for home page
function loaderTransition(){
    setTimeout(() => {
        loader.style.opacity = 0;
        loader.style.display = 'none';

        content.style.display = "block";
        nav.style.display="flex";
        setTimeout(() => {
            content.style.opacity = 1,50;
            nav.style.opacity = 1,50;
        })
        
       
    }, 2000);
}

loaderTransition()