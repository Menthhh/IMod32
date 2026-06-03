/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';
import './blocks/connection_blocks';
import './blocks/action_blocks';
import './blocks/text';
import './blocks/python_basics';
import { forBlock as modbusConnection } from './generators/python';
import { save, load } from './serialization';
import { toolbox } from './toolbox';
import './index.css';

Object.assign(pythonGenerator.forBlock, modbusConnection);
const codeDiv = document.getElementById('generatedCode').firstChild;
const outputDiv = document.getElementById('output');
const blocklyDiv = document.getElementById('blocklyDiv');
const ws = Blockly.inject(blocklyDiv, { toolbox });

const runCode = () => {
  const code = pythonGenerator.workspaceToCode(ws);
  codeDiv.innerText = code;
};

document.getElementById('runButton').addEventListener('click', () => {
  const code = pythonGenerator.workspaceToCode(ws);
  outputDiv.innerHTML = '';

  const Sk = window.Sk;
  if (!Sk) {
    outputDiv.innerHTML = '<span style="color:red">Skulpt not loaded. Check your internet connection.</span>';
    return;
  }

  Sk.configure({
    output: (text) => {
      const line = document.createElement('span');
      line.textContent = text;
      outputDiv.appendChild(line);
    },
    read: (url) => {
      if (Sk.builtinFiles?.files[url] === undefined)
        throw new Error(`File not found: '${url}'`);
      return Sk.builtinFiles.files[url];
    },
    inputfun: (prompt) => window.prompt(prompt) ?? '',
    inputfunTakesPrompt: true,
  });

  Sk.misceval.asyncToPromise(() =>
    Sk.importMainWithBody('<stdin>', false, code, true)
  ).catch((err) => {
    const errLine = document.createElement('span');
    errLine.style.color = 'red';
    errLine.textContent = err.toString();
    outputDiv.appendChild(errLine);
  });
});

// Load the initial state from storage and run the code.
load(ws);
runCode();

// Every time the workspace changes state, save the changes to storage.
ws.addChangeListener((e) => {
  // UI events are things like scrolling, zooming, etc.
  // No need to save after one of these.
  if (e.isUiEvent) return;
});

// Whenever the workspace changes meaningfully, run the code again.
ws.addChangeListener((e) => {
  // Don't run the code when the workspace finishes loading; we're
  // already running it once when the application starts.
  // Don't run the code during drags; we might have invalid state.
  if (
    e.isUiEvent ||
    e.type == Blockly.Events.FINISHED_LOADING ||
    ws.isDragging()
  ) {
    return;
  }
  runCode();
});
