import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';


export default {
    input: 'src/frontend/main.js',
    output: {
        name: 'HexchanJS',
        file: 'storage/frontend/scripts.js',
        format: 'iife',
        globals: {
            'jquery': '$',
            'lightbox2': 'lightbox',
        },
    },
    external: ['jquery', 'lightbox2'],
    plugins: [
        resolve(),
        commonjs(),
    ],
};
