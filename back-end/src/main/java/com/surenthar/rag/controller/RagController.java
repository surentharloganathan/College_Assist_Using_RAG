package com.surenthar.rag.controller;
import org.springframework.web.bind.annotation.CrossOrigin;

import com.surenthar.rag.dto.AnswerResponse;
import com.surenthar.rag.dto.QuestionRequest;
import com.surenthar.rag.service.RagService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:5173")

public class RagController {

    private final  RagService ragService;
    public RagController(RagService ragService) {
        this.ragService = ragService;
    }

    @PostMapping("/ask")
    public  AnswerResponse ask(@Valid @RequestBody QuestionRequest questionable)
    {
        return ragService.processanswer(questionable);
    }

}
