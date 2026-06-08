<template>
    <header class="header">
        <TheHeaderTitle title="Blog Sport" class="header__title"></TheHeaderTitle>
        <TheSearch class="header__search"></TheSearch>
        <TheNav class="header__nav"></TheNav>
        
        
    </header>
</template>


<style scoped>
.header{
    grid-column: 1/-1;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #2c3e50;
    color: #d4d3d3;
    padding: 5px;
    position: sticky;
    width: 100%;
    top: 0;
    z-index: 10;
    transition: top 0.2s;
    box-sizing: border-box;
}

</style>

<script setup>
import TheHeaderTitle from './TheHeaderTitle.vue';
import TheNav from '@/components/header/nav/TheNav.vue';
import TheSearch from '@/components/header/TheSearch.vue';
</script>