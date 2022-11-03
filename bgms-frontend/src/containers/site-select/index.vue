<template>
<div v-if="isVisible" class="site-select" :key="SiteSelectCurrentSiteId"> 
   
    <h3>Burial Grounds: </h3>
    <i class="icon-Clear-02-Filled cursor-pointer" @click="removeSelection"></i>



    <select v-if="inline" name="site_select" @change="selectSite($event.target.value)">                     
        <option v-for="site in allowedSitesFromBereavementStaff" :key="site.id" :value="site.id">
            {{ site.name}}
        </option>        
    </select>

    
    <ul v-else-if="allowedSitesFromBereavementStaff.length > 1" class="site-list">
        <li
            v-for="site in allowedSitesFromBereavementStaff"            
            :key="site.id"
            :class="{current:site == currentSite}"
        >
            <label class="flex items-center">
                <input
                    type="radio"
                    name="site-select"
                    :checked="site.id === currentSiteId"
                    @input="selectSite(site.id);"
                />
                <span>{{ site.name }}</span>
            </label>
        </li>
    </ul>
    <ul v-else class="site-list">
        <li
            v-for="site in allowedSitesFromBereavementStaff"            
            :key="site.id"
            :class="{current:site == currentSite}"
        >
            <label class="flex items-center">
                <input
                    type="radio"
                    name="site-select"
                    checked="True"
                    @input="selectSite(site.id);"
                    ref="singleInput"
                />
                <span>{{ site.name }}</span>
            </label>
        </li>
    </ul>
    
</div>
</template>

<style scoped src="./site-select.css"></style>

<script src="./site-select.js"></script>