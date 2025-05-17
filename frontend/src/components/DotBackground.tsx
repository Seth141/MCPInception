'use client';

import { useEffect, useRef, useState } from 'react';

interface Dot {
  x: number;
  y: number;
  size: number;
}

const DotBackground = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dots, setDots] = useState<Dot[]>([]);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const createDots = () => {
      if (!containerRef.current) return;
      
      const { width, height } = containerRef.current.getBoundingClientRect();
      const spacing = 50;
      const newDots: Dot[] = [];

      const cols = Math.ceil(width / spacing);
      const rows = Math.ceil(height / spacing);

      for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
          newDots.push({
            x: col * spacing,
            y: row * spacing,
            size: 2,
          });
        }
      }

      setDots(newDots);
    };

    createDots();
    window.addEventListener('resize', createDots);

    return () => {
      window.removeEventListener('resize', createDots);
    };
  }, []);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!containerRef.current) return;
    
    const rect = containerRef.current.getBoundingClientRect();
    setMousePosition({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 -z-10 overflow-hidden bg-black"
      onMouseMove={handleMouseMove}
    >
      {dots.map((dot, index) => {
        const distance = Math.sqrt(
          Math.pow(dot.x - mousePosition.x, 2) + Math.pow(dot.y - mousePosition.y, 2)
        );
        const maxDistance = 100; // Increased hover distance
        const isHovered = distance < maxDistance;
        const glowIntensity = Math.max(0, 1 - distance / maxDistance);
        
        return (
          <div
            key={index}
            className={`absolute rounded-full transition-all duration-200 ${
              isHovered 
                ? 'bg-white' 
                : 'bg-white/30'
            }`}
            style={{
              left: `${dot.x}px`,
              top: `${dot.y}px`,
              width: `${dot.size}px`,
              height: `${dot.size}px`,
              boxShadow: isHovered 
                ? `0 0 ${20 + glowIntensity * 30}px rgba(255, 255, 255, ${0.5 + glowIntensity * 0.5})`
                : 'none',
            }}
          />
        );
      })}
    </div>
  );
};

export default DotBackground; 