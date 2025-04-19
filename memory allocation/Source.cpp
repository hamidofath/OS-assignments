#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <iostream>
using namespace std;

#define TOTAL_MEMORY 500
#define BAR_WIDTH 50
bool compact_need= false;

typedef struct {
    int processId;
    int offset;
    int length;
    bool inUse;
} MemorySegment;

MemorySegment memLayout[100];
int segmentCount = 0;


void displayMemoryStatus() {
    printf("\n[Memory Allocation Table]\n");
    for (int i = 0; i < segmentCount; i++) {
        if (memLayout[i].inUse) {
            printf("[PID %d | Size %d | Offset %d]\n", memLayout[i].processId, memLayout[i].length, memLayout[i].offset);
        }
        else {
            printf("[FREE | Size %d | Offset %d]\n", memLayout[i].length, memLayout[i].offset);
            
        }
    }

 
    printf("-----------------------------\n");
}

void allocateProcess(int processId, int reqSize) {
    int offset = 0;

    for (int i = 0; i <= segmentCount; i++) {
        int gap = (i == segmentCount) ? TOTAL_MEMORY - offset : memLayout[i].offset - offset;

        if (gap >= reqSize) {
            for (int j = segmentCount; j > i; j--) {
                memLayout[j] = memLayout[j - 1];
            }
            memLayout[i].processId = processId;
            memLayout[i].offset = offset;
            memLayout[i].length = reqSize;
            memLayout[i].inUse = true;
            segmentCount++;
            printf("Allocated: PID %d | Size %d | Offset %d\n", processId, reqSize, offset);
            return;
        }

        if (i < segmentCount) {
            offset = memLayout[i].offset + memLayout[i].length;
        }
    }

    printf("Failed to allocate PID %d (Size %d): Not enough space.\n", processId, reqSize);
    if (compact_need) {
        printf("memory is needed to compact\n");
        
    }
}

void deallocateProcess(int processId) {
    for (int i = 0; i < segmentCount; i++) {
        if (memLayout[i].inUse && memLayout[i].processId == processId) {
            memLayout[i].inUse = false;
            printf("Deallocated process %d.\n", processId);
            compact_need = true;
            return;
        }
    }
    printf("Process %d not found.\n", processId);

}

void compactMemory() {
    
    int compactOffset = 0;

    for (int i = 0; i < segmentCount; i++) {
        if (memLayout[i].inUse) {
            if (memLayout[i].offset != compactOffset) {
                memLayout[i].offset = compactOffset;
            }
            compactOffset += memLayout[i].length;
        }
    }

    int newCount = 0;
    for (int i = 0; i < segmentCount; i++) {
        if (memLayout[i].inUse) {
            memLayout[newCount++] = memLayout[i];
        }
    }
    segmentCount = newCount;

    printf("Memory compacted.\n");
}

int main() {
    printf("Dynamic Memory Management Simulation\n");
    printf("-------------------------------\n");
    int action = 7;
    while (action == 7) {
        printf("1) allocate\n");
        printf("2) deallocate\n");
        printf("3) compact\n");
        printf("4) desplay\n");
        printf("5) end\n");
        printf("-----------------------------------\n");
        printf("enter the action you want:\n");

        cin >> action;
        if (action == 1) {
            int size, id;
            printf("enter the id and size of process to allocate:\n ");
            cin >> id >> size;
            allocateProcess(id, size);
        }
        if (action == 2) {
            int size, id;
            printf("enter the id and size of process to allocate:\n ");
            cin >> id ;
            deallocateProcess(id);

        }
        if (action == 3)
            compactMemory();
        if (action == 4)
            displayMemoryStatus();
        action = 7;

    }

    return 0;
}
