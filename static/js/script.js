// Three.js Setup
let scene, camera, renderer, car;

function initThreeJS() {
    const container = document.getElementById('canvas-container');
    
    scene = new THREE.Scene();
    
    camera = new THREE.PerspectiveCamera(
        35,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.set(0, 1.5, 6);
    
    renderer = new THREE.WebGLRenderer({ 
        antialias: true, 
        alpha: true 
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);
    
    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 10, 5);
    scene.add(directionalLight);
    
    const accentLight1 = new THREE.PointLight(0xff3d3d, 0.8);
    accentLight1.position.set(-3, 2, 2);
    scene.add(accentLight1);
    
    const accentLight2 = new THREE.PointLight(0xffef00, 0.6);
    accentLight2.position.set(3, 1, -2);
    scene.add(accentLight2);
    
    createCar();
    
    animate();
}

function createCar() {
    const carGroup = new THREE.Group();
    
    // Body
    const bodyGeometry = new THREE.BoxGeometry(2.5, 0.6, 1.2);
    const bodyMaterial = new THREE.MeshStandardMaterial({ 
        color: 0xff3d3d,
        metalness: 0.9,
        roughness: 0.1
    });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    body.position.y = 0.5;
    
    // Cabin
    const cabinGeometry = new THREE.BoxGeometry(1.5, 0.6, 1);
    const cabinMaterial = new THREE.MeshStandardMaterial({ 
        color: 0x3d3dff,
        metalness: 0.6,
        roughness: 0.2
    });
    const cabin = new THREE.Mesh(cabinGeometry, cabinMaterial);
    cabin.position.set(0, 1, 0);
    
    // Spoiler
    const spoilerGeometry = new THREE.BoxGeometry(1.2, 0.1, 0.8);
    const spoilerMaterial = new THREE.MeshStandardMaterial({ 
        color: 0x000000,
        metalness: 1,
        roughness: 0.2
    });
    const spoiler = new THREE.Mesh(spoilerGeometry, spoilerMaterial);
    spoiler.position.set(-1, 1.2, 0);
    
    // Wheels
    const wheelGeometry = new THREE.CylinderGeometry(0.35, 0.35, 0.25, 32);
    const wheelMaterial = new THREE.MeshStandardMaterial({ 
        color: 0x000000,
        metalness: 1,
        roughness: 0.1
    });
    
    const rimGeometry = new THREE.CylinderGeometry(0.2, 0.2, 0.27, 32);
    const rimMaterial = new THREE.MeshStandardMaterial({ 
        color: 0xffef00,
        metalness: 1,
        roughness: 0.2
    });
    
    const wheelPositions = [
        [-1, 0.35, 0.65],
        [-1, 0.35, -0.65],
        [1, 0.35, 0.65],
        [1, 0.35, -0.65]
    ];
    
    wheelPositions.forEach(pos => {
        const wheelGroup = new THREE.Group();
        
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        
        const rim = new THREE.Mesh(rimGeometry, rimMaterial);
        rim.rotation.z = Math.PI / 2;
        
        wheelGroup.add(wheel);
        wheelGroup.add(rim);
        wheelGroup.position.set(...pos);
        
        carGroup.add(wheelGroup);
    });
    
    carGroup.add(body);
    carGroup.add(cabin);
    carGroup.add(spoiler);
    
    car = carGroup;
    car.position.y = 0;
    car.rotation.y = Math.PI / 4;
    
    scene.add(car);
}

function animate() {
    requestAnimationFrame(animate);
    
    if (car) {
        car.rotation.y += 0.005;
        car.position.y = Math.sin(Date.now() * 0.001) * 0.15;
        
        // Rotate wheels
        car.children.forEach((child, index) => {
            if (index > 2) {
                child.children[0].rotation.x -= 0.05;
                child.children[1].rotation.x -= 0.05;
            }
        });
    }
    
    renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Locomotive Scroll Setup
const scroll = new LocomotiveScroll({
    el: document.querySelector('[data-scroll-container]'),
    smooth: true,
    multiplier: 0.8,
    lerp: 0.05
});

// GSAP ScrollTrigger Setup
gsap.registerPlugin(ScrollTrigger);

ScrollTrigger.scrollerProxy('[data-scroll-container]', {
    scrollTop(value) {
        return arguments.length 
            ? scroll.scrollTo(value, 0, 0) 
            : scroll.scroll.instance.scroll.y;
    },
    getBoundingClientRect() {
        return {
            top: 0,
            left: 0,
            width: window.innerWidth,
            height: window.innerHeight
        };
    },
    pinType: document.querySelector('[data-scroll-container]').style.transform 
        ? 'transform' 
        : 'fixed'
});

// Simple fade-in animations
gsap.utils.toArray('.case-card').forEach((card, i) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            scroller: '[data-scroll-container]',
            start: 'top 85%',
            toggleActions: 'play none none reverse'
        },
        y: 60,
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out'
    });
});

gsap.utils.toArray('.series-card').forEach((card, i) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            scroller: '[data-scroll-container]',
            start: 'top 85%',
            toggleActions: 'play none none reverse'
        },
        y: 60,
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out'
    });
});

gsap.utils.toArray('.treasure-card').forEach((card, i) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            scroller: '[data-scroll-container]',
            start: 'top 85%',
            toggleActions: 'play none none reverse'
        },
        scale: 0.9,
        opacity: 0,
        duration: 0.8,
        ease: 'back.out(1.2)'
    });
});

// Update ScrollTrigger
scroll.on('scroll', ScrollTrigger.update);
ScrollTrigger.addEventListener('refresh', () => scroll.update());
ScrollTrigger.refresh();

// Initialize
window.addEventListener('DOMContentLoaded', () => {
    initThreeJS();
});

window.addEventListener('load', () => {
    scroll.update();
    ScrollTrigger.refresh();
});
