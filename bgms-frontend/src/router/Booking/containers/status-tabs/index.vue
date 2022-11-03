<template>
<div class="status-tabs">
    <tabs
        v-model="selectedTab"
    >
        <!-- -->
        <div class="tab-group">
            <tab
                class="tab-wrapper"
                v-for="(tab, i) in tabs"
                :key="`t${i}`"
                :val="tab"
                :label="tab"
                :indicator="true"
            />
        </div>

        <!-- -->
        <div class="option-icons">
            <i class="fa fa-save"
               @click="submitStatus" 
            >

            </i>
            <!--<i class="fa fa-times"></i>-->
        </div>
    </tabs>
    <tab-panels
        v-model="selectedTab"
        :animate="false"
    >
        <tab-panel
            v-for="(tab, i) in tabs"
            :key="`tp${i}`"
            :val="tab"
        >
            <div class="status-content">
                <div v-if="i===0">
                  <div class="flex justify-between"  v-for="item in preburialList" :key="item.title">

                    <div class="flex w-2/4">
                      <div class="w-4 mr-5">
                      <input-field
                      type="checkbox"
                      v-model="item.active"
                      @change="function updateDateandUser(){item.date = item.active ? currentDate : null; item.username = item.active ? loggedInUser : null}"
                      />
                    </div>
                    <p>{{item.title}}</p>
                    </div>
                    <div class="w-1/4">
                      <div class="w-5/5 mb-3 mr-28">
                      <input-field
                      v-model="item.date"
                      :disabled="!item.active" 
                      type="date"
                      :max ="currentDate"
                      @format="format"                                            
                     />
                    </div>
                    
                    </div>
                     <div class="w-1/4">
                      <div class="w-5/5 mb-3 mr-28">    
                        <input-field
                            type="text"
                            v-model="item.username"
                            :disabled="true"
                        />
                      </div>
                    
                    </div>
                  </div>
                  
                </div>
                <div v-if="i===1 && !isPreBurialComplete">
                  <p>Please complete pre-burial checklist first.</p>
                </div>

                <div v-if="i===1 && isPreBurialComplete">
                  <div class="flex justify-between"  v-for="item in postburialList" :key="item.title">

                    <div class="flex w-2/4">
                      <div class="w-4 mr-5">
                      <input-field
                      type="checkbox"
                      v-model="item.active"
                      @change="function updateDateandUser(){item.date = item.active ? currentDate : null; item.username = item.active ? loggedInUser : null}"
                      />
                    </div>
                    <p>{{item.title}}</p>
                    </div>
                    <div class="w-1/4">
                      <div class="w-5/5 mb-3 mr-28">
                      <input-field
                      v-model="item.date"
                      :disabled="!item.active" 
                      type="date"
                      :max ="currentDate"
                      @format="format"
                      />
                      </div>                    
                    </div>
                     <div class="w-1/4">
                      <div class="w-5/5 mb-3 mr-28">    
                        <input-field
                            type="text"
                            v-model="item.username"
                            :disabled="true"
                        />
                      </div>                    
                    </div>  
                  
                  </div>
                </div>
                <div v-if="i===2">
                  <div class="form">
                      <div class="flex justify-between"  v-for="item in cancelburialList" :key="item.field">
                        <div class="flex-1">
                          <div class="mr-5">
                             <form-section-field label="Cancellation Reason:">
                              <input-field
                              type="textarea"
                              placeholder="Reason for Cancellation"
                              v-model="item.text"
                              @change="item.date = item.active ? currentDate : null"
                              />
                           </form-section-field>
                        </div>                    
                      </div>
                      <div>
                        <div class="w-5/5 mb-3">
                        <form-section-field>
                          <input-field
                          v-model="item.date"
                          type="date"
                          :max ="currentDate"
                          @format="format"
                        />
                       </form-section-field>
                      </div>
                    </div> 
                  </div>
                  </div>
                </div>
                
            </div>
        </tab-panel>
    </tab-panels>
     <notifications-list/>
</div>
</template>

<style scoped src="./status-tabs.css"></style>

<script src="./status-tabs.js"></script>
