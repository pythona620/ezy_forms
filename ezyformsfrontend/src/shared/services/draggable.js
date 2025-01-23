// useDragAndDrop.js

export const useDragAndDrop = () => {
    const handleDragStart = (event, index, type) => {
        // Store the dynamic data (index and type) for the dragged item
        const data = { index, type };
        event.dataTransfer.setData('text/plain', JSON.stringify(data)); // Store the data as JSON
    };

    const handleDragOver = (event) => {
        event.preventDefault(); // Allow the drop by preventing default handling
    };

    const handleDrop = (event, targetIndex, targetType) => {
        event.preventDefault();
        const draggedData = JSON.parse(event.dataTransfer.getData('text/plain'));
        const { index, type: draggedType } = draggedData;

        // Get the target element where the dragged item will be dropped
        const targetElement = event.target;

        // Handle dropping of sections
        if (draggedType === 'section' && targetType === 'section' && targetIndex === index) {
            const draggedSection = document.getElementById(targetElement.id);
            targetElement.appendChild(draggedSection); // Append the dragged section to the new position
        }

        // Handle dropping of columns
        if (draggedType === 'column' && targetType === 'column' && targetIndex === index) {
            const draggedColumn = document.getElementById(targetElement.id);
            targetElement.appendChild(draggedColumn); // Append the dragged column to the new position
        }

        // Handle dropping of fields
        if (draggedType === 'field' && targetType === 'field' && targetIndex === index) {
            const draggedField = document.getElementById(targetElement.id);
            targetElement.appendChild(draggedField); // Append the dragged field to the new position
        }
    };

    return { handleDragStart, handleDragOver, handleDrop };
};
