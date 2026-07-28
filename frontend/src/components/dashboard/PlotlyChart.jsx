import React, { useEffect, useRef } from 'react';

export default function PlotlyChart({ data, layout, config, style }) {
  const containerRef = useRef(null);

  useEffect(() => {
    // Load Plotly.js dynamically from CDN if not present globally
    if (window.Plotly) {
      window.Plotly.newPlot(containerRef.current, data, layout, config);
    } else {
      const script = document.createElement('script');
      script.src = 'https://cdn.plot.ly/plotly-2.30.0.min.js';
      script.async = true;
      script.onload = () => {
        if (window.Plotly && containerRef.current) {
          window.Plotly.newPlot(containerRef.current, data, layout, config);
        }
      };
      document.body.appendChild(script);
    }

    return () => {
      if (window.Plotly && containerRef.current) {
        window.Plotly.purge(containerRef.current);
      }
    };
  }, [data, layout, config]);

  return <div ref={containerRef} style={style || { width: '100%', height: '100%' }} />;
}
