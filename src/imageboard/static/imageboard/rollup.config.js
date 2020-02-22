const path = require('path');

export default {
    input: path.resolve(__dirname, 'main.js'),
    output: {
        name: 'HexchanJS',
        file: path.resolve(__dirname, 'hexchan.js'),
        format: 'iife',
        globals: {},
    },
    external: [],
    plugins: [],
};
