<template>
    <div class="container">
        <!-- Dynamic sections -->
        <div v-for="(section, sectionIndex) in sections" :key="'section-' + sectionIndex" class="draggable-section"
            :data-index="sectionIndex" @mousedown="startDrag($event, sectionIndex, 'section')"
            :style="{ top: section.top + 'px', left: section.left + 'px' }">
            <div>{{ section.name }}</div>

            <!-- Columns within the section -->
            <div v-for="(column, columnIndex) in section.columns" :key="'column-' + columnIndex"
                class="draggable-column" :data-index="columnIndex"
                @mousedown="startDrag($event, sectionIndex, columnIndex, 'column')"
                :style="{ top: column.top + 'px', left: column.left + 'px' }">
                <div>{{ column.name }}</div>

                <!-- Fields within the column -->
                <div v-for="(field, fieldIndex) in column.fields" :key="'field-' + fieldIndex" class="draggable-field"
                    :data-index="fieldIndex"
                    @mousedown="startDrag($event, sectionIndex, columnIndex, fieldIndex, 'field')"
                    :style="{ top: field.top + 'px', left: field.left + 'px' }">
                    <div>{{ field.name }}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const sections = ref([
    {
        name: 'Section 1',
        top: 50,
        left: 50,
        columns: [
            {
                name: 'Column 1',
                top: 50,
                left: 50,
                fields: [
                    { name: 'Field 1', top: 10, left: 10 },
                    { name: 'Field 2', top: 60, left: 10 },
                ],
            },
            {
                name: 'Column 2',
                top: 50,
                left: 200,
                fields: [
                    { name: 'Field 3', top: 10, left: 10 },
                    { name: 'Field 4', top: 60, left: 10 },
                ],
            },
        ],
    },
]);

let draggedItem = null;
let offsetX = 0;
let offsetY = 0;

const startDrag = (event, sectionIndex, columnIndex = null, fieldIndex = null, itemType = 'section') => {
    // Determine the dragged item
    if (itemType === 'section') {
        draggedItem = { type: 'section', index: sectionIndex };
    } else if (itemType === 'column') {
        draggedItem = { type: 'column', sectionIndex, index: columnIndex };
    } else if (itemType === 'field') {
        draggedItem = { type: 'field', sectionIndex, columnIndex, index: fieldIndex };
    }

    // Get initial offsets
    const item = getItem(draggedItem);
    offsetX = event.clientX - item.left;
    offsetY = event.clientY - item.top;

    window.addEventListener('mousemove', onDrag);
    window.addEventListener('mouseup', stopDrag);
};

const onDrag = (event) => {
    if (!draggedItem) return;
    const item = getItem(draggedItem);
    item.left = event.clientX - offsetX;
    item.top = event.clientY - offsetY;
};

const stopDrag = () => {
    window.removeEventListener('mousemove', onDrag);
    window.removeEventListener('mouseup', stopDrag);
    draggedItem = null;
};

const getItem = (draggedItem) => {
    if (draggedItem.type === 'section') {
        return sections.value[draggedItem.index];
    } else if (draggedItem.type === 'column') {
        return sections.value[draggedItem.sectionIndex].columns[draggedItem.index];
    } else if (draggedItem.type === 'field') {
        return sections.value[draggedItem.sectionIndex].columns[draggedItem.columnIndex].fields[draggedItem.index];
    }
    return {};
};
</script>

<style scoped>
.container {
    position: relative;
}

.draggable-section,
.draggable-column,
.draggable-field {
    position: absolute;
    padding: 10px;
    background-color: lightblue;
    border: 1px solid #ccc;
    cursor: move;
    user-select: none;
}

.draggable-section {
    background-color: lightgreen;
}

.draggable-column {
    background-color: lightcoral;
}

.draggable-field {
    background-color: lightyellow;
}
</style>